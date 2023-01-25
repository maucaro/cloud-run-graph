from flask import Flask, request
import networkx as nx
import logging as log
import urllib.request
import ssl
import os

file_url=os.environ.get("FILE_LOCATION", "https://storage.googleapis.com/synopsys-prod-maucaro/graph.adjlist")
port = int(os.environ.get("PORT", 8080))

def load_graph(file_url):
    context = ssl._create_unverified_context()
    file = urllib.request.urlopen(file_url, context = context)
    graph = nx.read_adjlist(path=file, nodetype=int)
    log.info(f'Loading done! Details: {graph}')
    return graph

graph = load_graph(file_url);

app = Flask(__name__)

@app.route("/connected", methods=['POST'])
def connected_api():
    request_json = request.get_json()
    start = request_json.get('start')
    end = request_json.get('end')
    try:
        shortest_path_len = len(nx.shortest_path(graph, start, end))
    except Exception as e:
        log.exception(e)
        shortest_path_len = -1
    result = "CONNECTED" if shortest_path_len > 0 else "DISCONNECTED"
    return {
        "result": result,
        "length": shortest_path_len,
        "start": start,
        "end": end
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)