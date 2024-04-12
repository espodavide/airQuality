package com.pollution.pollutionproject.citiesPollution;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.Collection;
import java.util.List;

@Service
public class citiesPollutionService {
    @Autowired
    citiesPollutionRepository repository;

    public List<citiesPollution> findAll() {
        return repository.findAll();
    }
    public Collection<citiesPollution> getCitiesHistoricalPollution(int id, LocalDate fromDate, LocalDate toDate){
        return repository.historicalDataPerCity(id,fromDate,toDate);
    }

    public Collection<citiesPollution> getCityHistoricalPollution(int id) {
        return repository.historicalAllDataPerCity(id);

    }
    public Collection<citiesPollution> getAllCitiesHistoricalPollution() {
        return repository.historicalAllDataAllCities();

    }
}
