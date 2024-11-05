package org.example;

import com.fasterxml.jackson.annotation.JsonProperty;
import scala.Tuple2;

import java.util.List;

public class WordCountOutputModel {
    String Word;
    int Count;

    public WordCountOutputModel(Tuple2<String, Integer> input) {
        this.Word = input._1();
        this.Count = input._2();
    }

    @JsonProperty
    public String getWord() {
        return this.Word;
    }

    @JsonProperty
    public int getCount() {
        return this.Count;
    }
}
