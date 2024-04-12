package com.pollution.pollutionproject.citiescoordinate;

import java.util.Collection;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1")
public class citiesCoordinateController {
    // aggiungere tutta la parte di risposta
    @Autowired
    private citiesCoordinateService citiesService;

    @GetMapping("/cities")
    public List<citiesCoordinate> getAllCities() {
        return citiesService.getAllCities();
    }
    @GetMapping("/cities/{id}")
    public citiesCoordinate getCity(@PathVariable Integer id ){
        return citiesService.getCityByID(id);
    }

    @PostMapping ("/cities")
    public ResponseEntity<citiesCoordinate> createCity(@RequestBody citiesCoordinate city ){
         citiesService.save(city);
        return new ResponseEntity<>(city, HttpStatus.CREATED);

    }
    @DeleteMapping("/cities/{id}")
    public  ResponseEntity<String> deleteCity(@PathVariable Integer id){
        String message = citiesService.delete(id);
        return new  ResponseEntity<>(message, HttpStatus.OK);
    }





}


