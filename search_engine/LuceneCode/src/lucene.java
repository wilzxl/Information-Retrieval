//package lucene;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import java.io.*;
import java.util.ArrayList;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class lucene {
//    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
	private  static ArrayList<String> filename = new ArrayList<>();
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
//	System.out.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");
//
	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
//	String s = br.readLine();
	String s = "Output/index";

	lucene indexer = null;
	try {
	    indexLocation = s;
	    indexer = new lucene(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		System.out.println("[Acceptable file types: .xml, .html, .html, .txt]");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "+ e.getMessage());
	    }
	}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);
	BufferedWriter bw = new BufferedWriter(new FileWriter(new File("Output/LuceneSE.txt")));
	int Qid = 0;
	s = "";
	while (!s.equalsIgnoreCase("q")) {
		Qid++;
		TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
		try {
		System.out.println("Enter the search query (q=quit):");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		Query q = new QueryParser(Version.LUCENE_47, "contents", sAnalyzer).parse(s);
			System.out.println(q);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
//		for (int i = 0; i < hits.length; ++i) {
//		    int docId = hits[i].doc;
//		    Document d = searcher.doc(docId);
//		    //query_id Q0 doc_id rank BM25_score system_name
//		    //System.out.println("1" +"\t" + "Q0" +"\t"+ d.get("filename").substring(0,d.get("filename").lastIndexOf("."))+ "\t\t\t\t\t\t"+i + "\t" + hits[i].score +"\t"+ "zhangxl_lucene");
//		    System.out.printf("%4d %4s %-50s %-4d %.6f %4s\n",Qid,"  Q0",d.get("filename").substring(0,d.get("filename").lastIndexOf(".")),i, hits[i].score,"  Lucene_SE");
//		}
			for (int i = 0; i < hits.length; ++i) {
				int docId = hits[i].doc;
				Document d = searcher.doc(docId);
				String str = d.get("filename");
				str = str.replace(".html", "");
				//System.out.println(Qid + " Q0 " + str + " " + (i+1) + " " + hits[i].score + " LuceneSE");
				bw.write(Integer.toString(Qid)+" Q0 "+str+" " +Integer.toString(i+1)+" "+String.valueOf(hits[i].score)+" Lucene_SE\n");
				System.out.printf("%3d %4s %-5s %-4d %.6f %4s\n",Qid,"  Q0",str,(i+1), hits[i].score,"  Lucene_SE");
			}
			bw.write("\n\n");
		// 5. term stats --> watch out for which "version" of the term
		// must be checked here instead!
		Term termInstance = new Term("contents", s);
		long termFreq = reader.totalTermFreq(termInstance);
		long docCount = reader.docFreq(termInstance);

		System.out.println(s + " Term Frequency " + termFreq + " - Document Frequency " + docCount);

	    } catch (Exception e) {
		System.out.println("Error searching " + s + " : "+ e.getMessage());
		break;
	    }

	}
		bw.close();
    }

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
	lucene(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);

	writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	//int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();

		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(), Field.Store.YES));

		writer.addDocument(doc);
		System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out.println((newNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} 
	else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
	    	queue.add(file);
	    } 
	    else {
	    	System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
    	writer.close();
    }
}