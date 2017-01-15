import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.StringTokenizer;
import java.lang.Iterable;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.*;

import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;

import org.apache.hadoop.util.*;
public class WordCount {
  public static class TokenizerMapper
       extends Mapper<LongWritable, Text, Text, Text>{
    private Text word = new Text();
    private static Set<String> Stopwords;
    static {
        Stopwords = new HashSet<String>();
        Stopwords.add("\","); Stopwords.add("&");Stopwords.add("\',");
        Stopwords.add("("); Stopwords.add(")");
    }
    public void map(LongWritable key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      int position = 0;
      while (itr.hasMoreTokens()) {
       String token = itr.nextToken();
       token.replaceAll("[{}:,]|(':)|('})|('},)|(:':)|(',)|('],)|(\n)", "");
       if (!Stopwords.contains(token)){
        word.set(token);
        position += 1;
        FileSplit split = (FileSplit)context.getInputSplit();
        String filename = split.getPath().getName();
        context.write(word, new Text(filename + "position:"+ position+ "count:1"));
       }else{
        position += 1;
       }
      }
} }
  public static class IntSumReducer
       extends Reducer<Text, Text, Text, Text> {
    Text result = new Text();
    public void reduce(Text key, Iterable <Text> values, Context context
        ) throws IOException, InterruptedException {
      int sum = 0;
      String files = new String();
      Text fileLocation = new Text();
      for (Text val : values) {
        String[] mapVar = val.toString().split("count:");
        files += mapVar[0];
        sum += 1;
      }
      result.set(new Text(sum + " "+ files));
      System.out.println("Reducer:");
      System.out.println(result);
      context.write(key, result);
    }
}
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "word count");
    job.setJarByClass(WordCount.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);
    job.setMapOutputKeyClass(Text.class);
    job.setMapOutputValueClass(Text.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(TextOutputFormat.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
} }
