package org.example;

import java.io.Console;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.SparkSession;
import org.jetbrains.annotations.NotNull;
import scala.Tuple2;


public class Main {


    public static void main(String[] args) {
        Queue<FileWordsOutputModel> FileResult = new LinkedList<FileWordsOutputModel>();
        String directoryPath = "C:\\Users\\49871\\Desktop\\PolyU\\Course\\projects\\comp5434bdc\\Partial\\pdf_json\\results";
        List<String> files = getAllFilePaths(directoryPath);
        SparkConf conf = new SparkConf().setAppName("map_reduce").setMaster("local[*]");
        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();
        JavaSparkContext sc = new JavaSparkContext(spark.sparkContext());
        for (String file : files) {
            List<String> data = readJsonFile(file);
            JavaRDD<String> words = sc.parallelize(data);
            //map words
            JavaPairRDD<String, Integer> oneWordCount = words.mapToPair(word -> new Tuple2<>(word, 1));
            //reduce words
            JavaPairRDD<String, Integer> counts = oneWordCount.reduceByKey(Integer::sum);

            List<Tuple2<String, Integer>> output = counts.collect();

            FileResult.add(new FileWordsOutputModel(getFileNameFromFullName(file), output));
        }
        while (!FileResult.isEmpty()) {
            FileWordsOutputModel file = FileResult.poll();
            writeJsonFile(directoryPath + "\\result", file.Name, file.WordCounts);
        }

        System.out.println("Mission complete.");
        sc.stop();
        spark.close();
    }

    private static List<String> getAllFilePaths(String directoryPath) {
        File directory = new File(directoryPath);
        File[] files = directory.listFiles();
        List<String> results = new ArrayList<String>();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    results.add(file.getAbsolutePath());
                }
            }
        }
        return results;
    }

    private static List<String> readJsonFile(String fileFullPath) {
        List<String> stringList;
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            stringList = objectMapper.readValue(new File(fileFullPath), new TypeReference<List<String>>() {
            });
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return stringList;
    }

    private static void writeJsonFile(String directoryPath, String fileName, List<WordCountOutputModel> results) {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.enable(SerializationFeature.INDENT_OUTPUT);
        try {
            // 手动拼接路径
            File outputFile = new File(directoryPath + "\\" + fileName);
            // 检查文件是否存在，如果不存在则创建
            if (!outputFile.exists()) {
                outputFile.getParentFile().mkdirs();
                outputFile.createNewFile();
            }
            objectMapper.writeValue(outputFile, results);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static @NotNull String getFileNameFromFullName(String fullName) {
        File file = new File(fullName);
        return file.getName();
    }
}