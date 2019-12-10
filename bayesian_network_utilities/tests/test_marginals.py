from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper
from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
from bayesian_network_utilities.api.event_merge_definition import EventMergeDefinition
from bayesian_network_utilities.tests import utilities
from bayesian_networks import *


def test_marginals_1__bake_network(bayesian_network_1):
    margs = bayesian_network_1.marginal()
    assert len(margs) == 2


def test_marginals_2__assert_marginals(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    margs = wrapper.get_marginals('j_gene')
    assert len(margs)==3


def test_marginals_3__merge_v_alleles(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.merge_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_marginals('v_gene')
    assert len(margs) == 2
    assert utilities.almost_equal(margs.get('V1'), 0.6, 0.0001)
    assert utilities.almost_equal(margs.get('V2*01'), 0.4, 0.0001)

def test_marginals_4__merge_j_alleles(bayesian_network_1):
    wrapper = BayesianNetworkWrapper(bayesian_network_1)
    merge_def1 = EventMergeDefinition('J1')
    merge_def1.extend(['J1*01', 'J1*02'])
    merge_defs = DistributionEventMergeDefinitions('j_gene', bayesian_network_1, allow_unspecified_events=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.merge_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_marginals('j_gene')
    assert len(margs) == 2
    assert utilities.almost_equal(margs.get('J1'), 0.77, 0.001)
    assert utilities.almost_equal(margs.get('J2*01'), 0.23, 0.001)


def test_marginals_5__merge_v_alleles(bayesian_network_2):
    wrapper = BayesianNetworkWrapper(bayesian_network_2)
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_2, allow_unspecified_events=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.merge_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_marginals('v_gene')
    assert len(margs) == 2
    assert utilities.almost_equal(margs.get('V1'), 0.6, 0.001)
    assert utilities.almost_equal(margs.get('V2*01'), 0.4, 0.001)

def test_marginals_6__merge_j_alleles(bayesian_network_2):
    wrapper = BayesianNetworkWrapper(bayesian_network_2)
    merge_def1 = EventMergeDefinition('J1')
    merge_def1.extend(['J1*01', 'J1*02'])
    merge_defs = DistributionEventMergeDefinitions('j_gene', bayesian_network_2, allow_unspecified_events=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.merge_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_marginals('j_gene')
    assert len(margs) == 2
    assert utilities.almost_equal(margs.get('J1'), 0.734, 0.001)
    assert utilities.almost_equal(margs.get('J2*01'), 0.266, 0.001)

def test_marginals_7__merge_j_alleles(bayesian_network_2):
    wrapper = BayesianNetworkWrapper(bayesian_network_2)
    merge_def1 = EventMergeDefinition('J1')
    merge_def1.extend(['J1*01', 'J1*02', 'J2*01'])
    merge_defs = DistributionEventMergeDefinitions('j_gene', bayesian_network_2, allow_unspecified_events=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.merge_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_marginals('j_gene')
    assert len(margs) == 1
    assert utilities.almost_equal(margs.get('J1'), 1.0, 0.001)

def test_marginals_8__merge_x_alleles(bayesian_network_2):
    wrapper = BayesianNetworkWrapper(bayesian_network_2)
    merge_def1 = EventMergeDefinition('X12')
    merge_def1.extend(['X1', 'X2'])
    merge_defs = DistributionEventMergeDefinitions('x_gene', bayesian_network_2, allow_unspecified_events=True)
    merge_defs.set_merge_definitions([merge_def1])
    merged_network = wrapper.merge_events(merge_defs)
    wrapper = BayesianNetworkWrapper(merged_network)
    margs = wrapper.get_marginals('x_gene')
    assert len(margs) == 1
    assert utilities.almost_equal(margs.get('X12'), 1.0, 0.001)
