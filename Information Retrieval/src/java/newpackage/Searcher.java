/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package newpackage;

import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
/**
 *
 * @author shwetimahajan
 */
public class Searcher {
    public class result
    {
        ArrayList <String> Names = new ArrayList();
        int Counter;
        
        result(ArrayList <String> st , int j)
        {
            Names = st;
            Counter = j;
        }
        
    }
    public ArrayList <String> searcherMethod(String key) throws IOException, ParseException {
            File dataDir = new File("/Users/vp/Downloads/Shweti/Movies"); //Directory containing data files in JSON format
            ArrayList <String> results = new ArrayList();  //variable to contain search results
            ArrayList <String> matchingMovies = new ArrayList();
            String keywords = key;
                                    
            //Lucene Code for Searching a query
            StandardAnalyzer stdan = new StandardAnalyzer();
            Query q = new QueryParser( "title", stdan).parse(keywords);
         // 3. search
            int hitsPerPage = 10;
            Directory indDir = FSDirectory.open(Paths.get("/Users/vp/Downloads/luindex"));
            IndexReader reader = DirectoryReader.open(indDir);
            IndexSearcher searcher = new IndexSearcher(reader);
            TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage);
            searcher.search(q, collector);
            ScoreDoc[] hits = collector.topDocs().scoreDocs;
    
            int count = 0;
         // 4. display results
            for(int i=0;i<hits.length;++i) {
            int docId = hits[i].doc;
            Document d = searcher.doc(docId);
            
            String nametemp = d.get("title");
            char x = 40;
            int y = nametemp.indexOf(x);
            String name = nametemp.substring(0, y);
            
            
            boolean flag = false;
            for(int j = 0 ; j < matchingMovies.size() ; j++)
            {
                if(name.equals(matchingMovies.get(j)))
                {
                    flag = true;
                    break;
                }
            }
            if(flag == false)
            {
                count = count + 1;
                matchingMovies.add(nametemp);
                System.out.println((count) + "\t" + name);
                //results.add(d.get("path"));
                //System.out.println(" Path :" + results.get(i));
            }
             // Code to retrieve the file names
            }
            reader.close();
            
            
            
            return matchingMovies;
    }
}
