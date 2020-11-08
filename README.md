# BlackDuck-Violator

Often third-party BlackDuck scans lack the policy settings for what license types you would consider an issue.
As a result, the CSV files mark all licenses as "Not In Violation", and fail to be imported as findings in <a href="https://github.com/DefectDojo/django-DefectDojo">DetectDojo</a>.

This script will rotate through a zip archive, or directory of zip archives, unpacking each one, locating the component.csv file, processing it for selected license types to be marked as "In Violation", then repacking the zip files.
