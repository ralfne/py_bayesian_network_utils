# from pomegranate.BayesianNetwork import BayesianNetwork
# from pomegranate.base import Node
# from pomegranate.distributions.ConditionalProbabilityTable import ConditionalProbabilityTable
# from pomegranate.distributions.DiscreteDistribution import DiscreteDistribution
#
# from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper
# from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
# from bayesian_network_utilities.api.event_merge_definition import EventMergeDefinition
#
#
# def bayesian_network_3():
#     v_gene = DiscreteDistribution({'V1*01': 0.3, 'V1*02': 0.1, 'V2*01': 0.6})
#     j_gene = ConditionalProbabilityTable([['V1*01', 'J1*01', 0.1], ['V1*01', 'J2*01', 0.9],
#                                           ['V1*02', 'J1*01', 0.4], ['V1*02', 'J2*01', 0.6],
#                                           ['V2*01', 'J1*01', 0.2], ['V2*01', 'J2*01', 0.8]],
#                                         [v_gene])
#     v_del = ConditionalProbabilityTable([['V1*01', 'vdel:1', 0.7], ['V1*01', 'vdel:2', 0.3],
#                                           ['V1*02', 'vdel:1', 0.9], ['V1*02', 'vdel:2', 0.1],
#                                           ['V2*01', 'vdel:1', 0.5], ['V2*01', 'vdel:2', 0.5]],
#                                          [v_gene])
#     j_del = ConditionalProbabilityTable([['J1*01', 'jdel:1', 0.6], ['J1*01', 'jdel:2', 0.4],
#                                          ['J2*01', 'jdel:1', 0.7], ['J2*01', 'jdel:2', 0.3]],
#                                         [j_gene])
#     d_gene = ConditionalProbabilityTable([['V1*01', 'J1*01', 'D1*01', 0.6], ['V1*01', 'J1*01', 'D2*01', 0.4],
#                                           ['V1*01', 'J2*01', 'D1*01', 0.3], ['V1*01', 'J2*01', 'D2*01', 0.7],
#                                           ['V1*02', 'J1*01', 'D1*01', 0.7], ['V1*02', 'J1*01', 'D2*01', 0.3],
#                                           ['V1*02', 'J2*01', 'D1*01', 0.1], ['V1*02', 'J2*01', 'D2*01', 0.9],
#                                           ['V2*01', 'J1*01', 'D1*01', 0.1], ['V2*01', 'J1*01', 'D2*01', 0.9],
#                                           ['V2*01', 'J2*01', 'D1*01', 0.5], ['V2*01', 'J2*01', 'D2*01', 0.5]],
#                                         [v_gene, j_gene])
#     d_5_del = ConditionalProbabilityTable([['D1*01', 'ddel5:1', 0.2], ['D1*01', 'ddel5:2', 0.8],
#                                          ['D2*01', 'ddel5:1', 0.3], ['D2*01', 'ddel5:2', 0.7]],
#                                         [d_gene])
#     d_3_del = ConditionalProbabilityTable([['D1*01', 'ddel5:1', '1', 0.6], ['D1*01', 'ddel5:1', '2', 0.4],
#                                            ['D1*01', 'ddel5:2', '1', 0.2], ['D1*01', 'ddel5:2', '2', 0.8],
#                                            ['D2*01', 'ddel5:1', '1', 0.9], ['D2*01', 'ddel5:1', '2', 0.1],
#                                            ['D2*01', 'ddel5:2', '1', 0.0], ['D2*01', 'ddel5:2', '2', 1.0]],
#                                           [d_gene, d_5_del])
#     v_gene_node = Node(v_gene, name="v_gene")
#     j_gene_node = Node(j_gene, name="j_gene")
#     d_gene_node = Node(d_gene, name="d_gene")
#     v_del_node = Node(v_del, name="v_del")
#     j_del_node = Node(j_del, name="j_del")
#     d_5_del_node = Node(d_5_del, name="d_5_del")
#     d_3_del_node = Node(d_3_del, name="d_3_del")
#     out = BayesianNetwork("VDJ")
#     out.add_states(v_gene_node, j_gene_node, d_gene_node, v_del_node, j_del_node, d_5_del_node, d_3_del_node)
#     out.add_edge(v_gene_node, j_gene_node)
#     out.add_edge(v_gene_node, v_del_node)
#     out.add_edge(j_gene_node, j_del_node)
#     out.add_edge(v_gene_node, d_gene_node)
#     out.add_edge(j_gene_node, d_gene_node)
#     out.add_edge(d_gene_node, d_5_del_node)
#     out.add_edge(d_gene_node, d_3_del_node)
#     out.add_edge(d_5_del_node, d_3_del_node)
#     out.bake()
#     return out
#
# bn = bayesian_network_3()
#
# merge_def1 = EventMergeDefinition('V1')
# merge_def1.extend(['V1*01', 'V1*02'])
# merge_defs = DistributionEventMergeDefinitions('v_gene', bn, allow_unspecified_events=True,
#                                                assert_merge_definitions=True)
#
# merge_defs.set_merge_definitions([merge_def1])
# wrapper = BayesianNetworkWrapper(bn)
# merged_network = wrapper.create_network_with_merged_events(merge_defs)
# wrapper = BayesianNetworkWrapper(merged_network)
# print 3