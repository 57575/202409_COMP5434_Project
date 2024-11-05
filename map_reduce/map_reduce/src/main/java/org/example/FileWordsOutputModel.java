package org.example;

import scala.Tuple2;

import java.util.ArrayList;
import java.util.List;

public class FileWordsOutputModel {
    String Name;
    List<WordCountOutputModel> WordCounts;

    public FileWordsOutputModel(String name, List<Tuple2<String, Integer>> wordCounts) {
        this.Name = name;
        this.WordCounts = new ArrayList<>();
        for (Tuple2<String, Integer> wordCount : wordCounts) {
            this.WordCounts.add(new WordCountOutputModel(wordCount));
        }
    }
}
