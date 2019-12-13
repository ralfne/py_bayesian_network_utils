from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper
from bayesian_networks import *


def test_comparisons_1__compare_structure(bayesian_network_1):
    wrapper1 = BayesianNetworkWrapper(bayesian_network_1)
    wrapper2 = BayesianNetworkWrapper(bayesian_network_1)
    wrapper1.assert_structure_equality(wrapper2)


def test_comparisons_2__compare_structure(bayesian_network_1, bayesian_network_2):
    wrapper1 = BayesianNetworkWrapper(bayesian_network_1)
    wrapper2 = BayesianNetworkWrapper(bayesian_network_2)
    with pytest.raises(Exception) as e:
        assert wrapper1.assert_structure_equality(wrapper2)
    assert str(e.value) == 'Number of states not equal'
