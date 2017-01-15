from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, json, math

PORT_NUMBER = 8081

class BM25:
    def __init__(self):
        self.parsedContent = {}
        self.k1 = 1.2
        self.b = 0.75
        self.N = 0
        self.k2 = 100

    def load_json_file(self):
        moviesKeyList = []
        with open('jsonFormat', 'r') as content_file:
            content = content_file.read()
            self.parsedContent = json.loads(content)
            for key in self.parsedContent:
                for k in self.parsedContent[key]['locations']:
                    if k not in moviesKeyList:
                        moviesKeyList.append(k)
        self.N = len(moviesKeyList)

    def parse_query(self, query):
        queryString = query.split('=').pop().split('%20')
        i = 0
        for q in queryString:
            queryString[i] = q.lower()
            i += 1
        documentList = {}
        queryList = {}
        for qryStr in queryString:
            try:
                value = self.parsedContent[qryStr]
                if qryStr not in queryList:
                    queryList[qryStr] = 1
                else:
                    queryList[qryStr] += 1
                for v in value['locations']:
                    if v not in documentList:
                        documentList[v] = {}
                        documentList[v][qryStr] = len(value['locations'][v])
                    else:
                        documentList[v][qryStr] = len(value['locations'][v])
            except:
                return 'Not found'
        score = []
        for d in documentList:
            if 'TVSeries.txt' != d:
                score.append([d, self.compute_score(d, documentList[d], queryList)])
        score.sort(key=lambda x: x[1], reverse=True)
        print score
        return score

    def compute_score(self, d, dList, qList):
        fileName = d+'-IMDb.txt'
        f = open('Movies/Movies/'+fileName, 'r').read()
        dl = len(f.split(' '))
        K = self.k1*((1-self.b)+self.b*dl/500)
        score = 0
        n = len(dList)
        for val in dList:
            if val in d:
                score += 2*math.log(1/((n + 0.5)/(self.N-n+.5))) * ((self.k1+1)*dList[val]/(K+dList[val])) * ((self.k2+1)*qList[val]/(self.k2+qList[val]))
            else:
                score += math.log(1/((n + 0.5)/(self.N-n+.5))) * ((self.k1+1)*dList[val]/(K+dList[val])) * ((self.k2+1)*qList[val]/(self.k2+qList[val]))
        return score

    def run(self, query):
        self.load_json_file()
        return self.parse_query(query)

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        score = BM25();
        tempValue = score.run(parsed_path.query.split('&')[0])
        message_parts.append("ResultList:"+str(tempValue))
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        # self.end_headers()
        self.wfile.write(message)
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', PORT_NUMBER), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
