Fill in the firebaseConfig with information from Firebase console.

To run flask with firebase admin (to check the idtoken validity), service account json is required:

```bash
sudo pip install firebase-admin
FLASK_APP=app FLASK_ENV=development GOOGLE_APPLICATION_CREDENTIALS=<path-to-service-account-.json> flask run
```
