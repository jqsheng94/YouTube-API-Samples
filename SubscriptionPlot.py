import csv
import networkx as nx
import matplotlib.pyplot as plt
import requests
from urllib.request import urlopen
import simplejson as json
import SubscriptionList as Sub
import itertools


G = nx.Graph()
DefaulChannel = "UCaK87UTTMacD35eQITej2VA"
Results = Sub.retrieveSubscriptionList(channelID = DefaulChannel).main()
FullList = [DefaulChannel] + Results
if len(Results) >= 1:
    SecondLayer = []
    ThirdLayer = []
    for sender in Results:
        G.add_edge(DefaulChannel, sender)
        SecondLayer.append(sender)
        recipients = Sub.retrieveSubscriptionList(channelID=sender).main()
        FullList += recipients
        for recipient in recipients:
            G.add_edge(sender, recipient)
            if recipient not in SecondLayer and recipient not in ThirdLayer:
                ThirdLayer.append(recipient)
    for i in ThirdLayer:
        connections = Sub.retrieveSubscriptionList(channelID=i).main()
        common = [i for i in connections if i in FullList]
        for t in common:
            G.add_edge(recipient, t)
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos, nodelist=G, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=ThirdLayer, node_color=range(len(ThirdLayer)), with_labels=False, font_size=0, node_size=200, cmap=plt.cm.Reds)
    nx.draw_networkx_nodes(G, pos, nodelist=SecondLayer, node_color=range(len(SecondLayer)), with_labels=False, font_size=0, node_size=300, cmap=plt.cm.Blues)
    nx.draw_networkx_nodes(G, pos, nodelist=[DefaulChannel], node_color='yellow', font_size=12, node_size=500)
    plt.title('Channel ' + DefaulChannel + ' Subscription Network Plot')
    plt.savefig('./fig/SubscriptionNetworkPlot.png')
else:
    print('No Accees to Channel ' + DefaulChannel)



