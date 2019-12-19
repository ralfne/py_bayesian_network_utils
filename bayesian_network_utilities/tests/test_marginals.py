from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper, ProbabilityType
from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
from bayesian_network_utilities.api.event_merge_definition import EventMergeDefinition
from bayesian_network_utilities.tests import utilities
from bayesian_networks import *


def test_marginals_1__bake_network(bayesian_network_1):
    margs = bayesian_network_1.marginal()
    assert len(margs) == 2


def test_marginals_2__assert_marginals(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    margs = wrapper.get_probabilities('j_gene', ProbabilityType.Marginal)
    assert len(margs)==3


def test_marginals_3__merge_v_alleles(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.create_network_with_merged_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_probabilities(statename='v_gene', probability_type=ProbabilityType.Marginal)
    assert len(margs) == 2
    assert utilities.almost_equal(margs['V1'], 0.6, 0.0001)
    assert utilities.almost_equal(margs['V2*01'], 0.4, 0.0001)


def test_marginals_4__merge_v_alleles(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.create_network_with_merged_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_probabilities(statename=None, probability_type=ProbabilityType.Marginal)
    assert len(margs) == 2
    for key, value in margs.iteritems():
        tot = value.sum()
        assert utilities.almost_equal(tot, 1.0, 0.0001)

def test_marginals_5__merge_v_alleles(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.create_network_with_merged_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_probabilities(statename='v_gene', probability_type=ProbabilityType.Conditional)
    assert len(margs) == 2
    assert utilities.almost_equal(margs.iloc[0,0], 0.6, 0.0001)
    assert utilities.almost_equal(margs.iloc[1,0], 0.4, 0.0001)


def test_marginals_6__merge_v_alleles(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.create_network_with_merged_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_probabilities(statename=None, probability_type=ProbabilityType.Conditional)
    assert len(margs) == 2
    tot = margs[margs.keys()[0]].loc[:, 'p'].sum()
    assert utilities.almost_equal(tot, 1.0, 0.0001)
    tot = margs[margs.keys()[1]].loc[:, 'p'].sum()
    assert utilities.almost_equal(tot, 2.0, 0.0001)


def test_marginals_7__merge_all_alleles(bayesian_network_3):
    wrapper = BayesianNetworkWrapper(bayesian_network_3)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', wrapper.get_network(), allow_unspecified_events=True,
                                                   assert_merge_definitions=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.create_network_with_merged_events(merge_defs)
    assert (merged_network is not None)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_probabilities(statename=None, probability_type=ProbabilityType.Conditional)
    assert len(margs) == 7
