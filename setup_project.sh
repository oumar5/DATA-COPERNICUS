#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e



# 2. Create top-level files
touch app.py requirements.txt README.md

# 3. Create the 'config' folder and files
mkdir -p config
touch config/__init__.py config/config.py config/utils.py

# 4. Create the 'data' folder and files
mkdir -p data
touch data/__init__.py data/data_loader.py data/database.py

# 5. Create the 'modules' folder with subfolders for each feature
mkdir -p modules
touch modules/__init__.py

# Soil monitoring module
mkdir -p modules/soil_monitoring
touch modules/soil_monitoring/__init__.py \
      modules/soil_monitoring/page.py \
      modules/soil_monitoring/components.py \
      modules/soil_monitoring/service.py

# Irrigation module
mkdir -p modules/irrigation
touch modules/irrigation/__init__.py \
      modules/irrigation/page.py \
      modules/irrigation/components.py \
      modules/irrigation/service.py

# Climatic analysis module
mkdir -p modules/climatic_analysis
touch modules/climatic_analysis/__init__.py \
      modules/climatic_analysis/page.py \
      modules/climatic_analysis/components.py \
      modules/climatic_analysis/service.py

# 6. Create the 'pages' folder and files
mkdir -p pages
touch pages/__init__.py pages/home.py pages/about.py

# 7. Create the 'assets' folder and files
mkdir -p assets
touch assets/styles.css assets/logo.png

# 8. Create the 'tests' folder and files
mkdir -p tests
touch tests/__init__.py tests/test_soil_monitoring.py tests/test_utils.py

echo "Project structure created successfully!"
