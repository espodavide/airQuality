package com.pollution.pollutionproject.citiesPollution;

import org.springframework.cglib.core.Local;

import java.time.LocalDate;

public class pollutionRequest {
    LocalDate fromDate;

    LocalDate toDate;

    public pollutionRequest(LocalDate fromDate, LocalDate toDate) {
        this.fromDate = fromDate;
        this.toDate = toDate;
    }

    public LocalDate getFromDate() {
        return fromDate;
    }

    public void setFromDate(LocalDate fromDate) {
        this.fromDate = fromDate;
    }

    public LocalDate getToDate() {
        return toDate;
    }

    public void setToDate(LocalDate toDate) {
        this.toDate = toDate;
    }
}
