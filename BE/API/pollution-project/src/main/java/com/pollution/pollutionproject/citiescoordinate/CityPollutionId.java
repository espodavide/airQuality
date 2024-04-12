package com.pollution.pollutionproject.citiescoordinate;

import java.io.Serializable;
import java.time.LocalDate;

public class CityPollutionId implements Serializable {
    public CityPollutionId(){
        super();
    }
    private int CITY_ID;
    private LocalDate DATE;

    public CityPollutionId(int CITY_ID, LocalDate DATE) {
        this.CITY_ID = CITY_ID;
        this.DATE = DATE;
    }

    public int getCITY_ID() {
        return CITY_ID;
    }

    public void setCITY_ID(int CITY_ID) {
        this.CITY_ID = CITY_ID;
    }

    public LocalDate getDATE() {
        return DATE;
    }

    public void setDATE(LocalDate DATE) {
        this.DATE = DATE;
    }
}
