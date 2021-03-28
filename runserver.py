"""
Runs the application
"""

from inz_irma_backend.backend import app

app.run('0.0.0.0', 5050, debug=True)
