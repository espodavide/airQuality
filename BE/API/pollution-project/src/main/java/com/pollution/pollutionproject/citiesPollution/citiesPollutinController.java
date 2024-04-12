package com.pollution.pollutionproject.citiesPollution;

import com.sun.tools.javac.Main;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.Collection;
import java.util.List;
import java.util.logging.Logger;

@RestController
public class citiesPollutinController {
    Logger logger = Logger.getLogger(Main.class.getName());

    @Autowired
    citiesPollutionService service;

    @GetMapping("/cities-pollution")
    public List<citiesPollution> getAllCitiesPollution(){
        return service.findAll();
    }

    @GetMapping("/cities-pollution-historical-data/{id}")
    public Collection<citiesPollution> getCitiesHistoricalPollution(@PathVariable int id,
                                                                    @RequestBody pollutionRequest pollutionRequest ) {
        LocalDate fromDate = pollutionRequest.getFromDate();
        LocalDate toDate = pollutionRequest.getToDate();

        logger.warning(id+" dateFrom: "+fromDate+" dateTo "+toDate);
        return service.getCitiesHistoricalPollution(id,fromDate,toDate);
    }
    @GetMapping("/cities-pollution-all-historical-data/{id}")
    public Collection<citiesPollution> getCitiesAllHistoricalPollution(@PathVariable int id ) {
        return service.getCityHistoricalPollution(id);
    }
    @GetMapping("/cities-pollution-all-historical-data")
    public Collection<citiesPollution> getAllCitiesAllHistoricalPollution( ) {
        return service.getAllCitiesHistoricalPollution();
    }

}
