from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
from bayesian_network_utilities.api.event_merge_definition import EventMergeDefinition
from bayesian_networks import *


def test_merge_definitions_1__distribution_not_found(bayesian_network_1):
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('x_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    with pytest.raises(ValueError) as e:
        merge_defs.set_merge_definitions([merge_def1])
    assert str(e.value) == DistributionEventMergeDefinitions.ERR_DIST_NAME_NOT_FOUND_MSG


def test_merge_definitions_2__event_not_found(bayesian_network_1):
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*04'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    with pytest.raises(ValueError) as e:
        merge_defs.set_merge_definitions([merge_def1])
    assert str(e.value) == DistributionEventMergeDefinitions.ERR_EVENT_NOT_FOUND


def test_merge_definitions_3__duplicated_events(bayesian_network_1):
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*02'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True, assert_merge_definitions=True)
    with pytest.raises(ValueError) as e:
        merge_defs.set_merge_definitions([merge_def1])
    assert str(e.value) == DistributionEventMergeDefinitions.ERR_DUPLICATE_EVENT_MSG


def test_merge_definitions_4__unspecified_event(bayesian_network_1):
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=False,
                                                                                assert_merge_definitions=True)
    with pytest.raises(ValueError) as e:
        merge_defs.set_merge_definitions([merge_def1])
    assert str(e.value) == DistributionEventMergeDefinitions.ERR_UNSPECIFIED_EVENTS_NOT_ALLOWED_MSG


def test_merge_definitions_5__one_merge_def_only(bayesian_network_1):
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    merge_def2 = EventMergeDefinition('V2')
    merge_def2.extend(['V2*01'])
    merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_1, allow_unspecified_events=True,
                                                                                assert_merge_definitions=True)
    with pytest.raises(ValueError) as e:
        merge_defs.set_merge_definitions([merge_def1, merge_def2])
    assert str(e.value) == DistributionEventMergeDefinitions.ERR_ONLY_ONE_MERGE_DEF_ALLOWED_MSG


def test_merge_definitions_6__events_not_unique(bayesian_network_0):
    merge_def1 = EventMergeDefinition('V1')
    merge_def1.extend(['V1*01', 'V1*02', 'V1*03'])
    with pytest.raises(ValueError) as e:
        merge_defs = DistributionEventMergeDefinitions('v_gene', bayesian_network_0, allow_unspecified_events=True,
                                                                                    assert_merge_definitions=True)
    assert str(e.value) == DistributionEventMergeDefinitions.ERR_NETWORK_HAS_DUPLICATED_EVENT_NAMES


