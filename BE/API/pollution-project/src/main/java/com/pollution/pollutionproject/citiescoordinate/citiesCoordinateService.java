package com.pollution.pollutionproject.citiescoordinate;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Collection;
import java.util.List;

@Service
public class citiesCoordinateService {
    @Autowired
    citiesCoordinateRepository cityRepository;

    public List<citiesCoordinate> getAllCities(){
        return cityRepository.findAll();
    }

    public citiesCoordinate getCityByID(Integer id){
        return cityRepository.findById(id).get();
    }

    public void save(citiesCoordinate city) {
        cityRepository.save(city);
    }

    public String delete(Integer id) {
        String cityName=cityRepository.findById(id).get().getName();
        cityRepository.deleteById(id);
        return "The city: "+ cityName +" with ID: "+ id + " has been deleted";
    }
}
