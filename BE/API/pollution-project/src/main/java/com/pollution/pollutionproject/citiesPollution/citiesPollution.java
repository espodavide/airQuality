package com.pollution.pollutionproject.citiesPollution;


import com.pollution.pollutionproject.citiescoordinate.CityPollutionId;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;

import java.time.LocalDate;

@Entity(name ="CITIES_POLLUTION")
@IdClass(CityPollutionId.class)
public class citiesPollution {
    public citiesPollution(){
        super();
    }

    int AQI ;
    float CO ;
    float NO ;
    float NO2 ;
    float O3 ;
    float SO2 ;
    float PM2_5 ;
    float PM10 ;
    float NH3 ;
    float DT ;
    String CITY ;
    @Id
    int CITY_ID ;
    @Id
    LocalDate DATE ;

    public citiesPollution(int AQI, float CO, float NO, float NO2, float o3, float SO2, float PM2_5, float PM10, float NH3, float DT, String CITY, int CITY_ID, LocalDate DATE) {
        this.AQI = AQI;
        this.CO = CO;
        this.NO = NO;
        this.NO2 = NO2;
        this.O3 = o3;
        this.SO2 = SO2;
        this.PM2_5 = PM2_5;
        this.PM10 = PM10;
        this.NH3 = NH3;
        this.DT = DT;
        this.CITY = CITY;
        this.CITY_ID = CITY_ID;
        this.DATE = DATE;
    }

    public int getAQI() {
        return AQI;
    }

    public void setAQI(int AQI) {
        this.AQI = AQI;
    }

    public float getCO() {
        return CO;
    }

    public void setCO(float CO) {
        this.CO = CO;
    }

    public float getNO() {
        return NO;
    }

    public void setNO(float NO) {
        this.NO = NO;
    }

    public float getNO2() {
        return NO2;
    }

    public void setNO2(float NO2) {
        this.NO2 = NO2;
    }

    public float getO3() {
        return O3;
    }

    public void setO3(float o3) {
        O3 = o3;
    }

    public float getSO2() {
        return SO2;
    }

    public void setSO2(float SO2) {
        this.SO2 = SO2;
    }

    public float getPM2_5() {
        return PM2_5;
    }

    public void setPM2_5(float PM2_5) {
        this.PM2_5 = PM2_5;
    }

    public float getPM10() {
        return PM10;
    }

    public void setPM10(float PM10) {
        this.PM10 = PM10;
    }

    public float getNH3() {
        return NH3;
    }

    public void setNH3(float NH3) {
        this.NH3 = NH3;
    }

    public float getDT() {
        return DT;
    }

    public void setDT(float DT) {
        this.DT = DT;
    }

    public String getCITY() {
        return CITY;
    }

    public void setCITY(String CITY) {
        this.CITY = CITY;
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
