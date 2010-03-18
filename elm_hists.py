""" Plot comparitive histograms
    of sequence distributions.

    Enter host ELM results,
    flu ELM results,
    and species name for flu file.

    This will output out seq count
    bar graphs for each ELM.
"""
import utils_plot, sys, os
from collections import defaultdict

def get_test_data():
    #test_data1 = utils_plot.mk_test_data()
    #test_data2 = utils_plot.mk_test_data()
    #return [test_data1, test_data2]
    return utils_plot.mk_test_data()

def test_plot_old():
    """ Makes test data """

    [test_data1, test_data2] = get_test_data()
    
    print 'Set\tSeq\tCount'
    for name, a_set in [['set1',
                         test_data1], 
                        ['set2',
                         test_data2]]:
        for k in a_set:
            print name + '\tAAAA' + k + '\t' + str(a_set[k])

def test_plot():
    [test_data1, test_data2] = get_test_data()
    utils_plot.elm_freq_histogram(test_data1, 'human',
                                  test_data2, 'virus',
                                  'test.png', 'LIG_TEST')

def get_seq2count_dict(elm_file, cutoff):
    elm2seq2count = defaultdict(dict)
    with open(elm_file) as f:
        for line in f:
            [elm, seq, count, frac_st] = line.strip().split('\t')
            frac = float(frac_st)
            if frac >= cutoff:
                elm2seq2count[elm][seq] = frac
    return elm2seq2count

def check_ones(species2elms, elm):
    """ Is there only one sequence for this ELM
        in all species """

    not_one = False

    for species in species2elms:
        if len(species2elms[species][elm].keys()) > 1:
            not_one = True
            break
    return not_one

def main(args):
    file_species_pairs = []
    i = 1
    while i < len(args)-2:
        file_species_pairs.append([args[i], args[i+1]])
        i += 2

    cutoff = float(sys.argv[-2])
    plot_dir = sys.argv[-1]

    species2elms = {}
    for file, species in file_species_pairs:
        species2elms[species] = get_seq2count_dict(file, cutoff)

    elms = {}
    for species in species2elms:
        for elm in species2elms[species]:
            elms[elm] = True
    for elm in elms:
        if check_ones(species2elms, elm):
            utils_plot.elm_host_barplot(species2elms, elm,
                                        os.path.join(plot_dir,
                                                     elm + '.hosts.png'))

if __name__ == '__main__': main(sys.argv)

