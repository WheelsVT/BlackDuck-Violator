# BlackDuck-Violator

Often third-party BlackDuck scans lack the policy settings for what license types you would consider an issue.
As a result, the CSV files mark all licenses as "Not In Violation".

A PR has been submitted to <a href="https://github.com/DefectDojo/django-DefectDojo">DetectDojo</a> for added functionality to import "Not In Violation" license risks when a license severity is present as license risks for review.

This companion script will rotate through a BlackDuck zip archive, or directory of zip archives, unpacking each one, locating the component.csv file, processing it for selected license types to be marked as "In Violation" or modify review severity level, then repacking the zip files.

This allows organizations to set their own rules/policies for licenses outside of BlackDuck prior to import into DefectDojo for tracking triage and resolution.
