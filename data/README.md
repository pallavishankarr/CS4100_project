# Data Directory

This directory contains the Yelp business dataset.

## Dataset File

**File**: `yelp_academic_dataset_business.json`

**Size**: ~113 MB

**Note**: This file is excluded from git due to GitHub's 100 MB file size limit. 

## Obtaining the Dataset

The Yelp Open Dataset can be downloaded from:
- [Yelp Open Dataset](https://www.yelp.com/dataset)

Place the `yelp_academic_dataset_business.json` file in this directory to run the application.

## Dataset Format

The file is in JSON Lines format (one JSON object per line), containing business information including:
- Business ID, name, address
- Location (city, state, postal code, coordinates)
- Ratings (stars, review count)
- Categories and attributes
- Operating hours

