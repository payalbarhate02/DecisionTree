import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained Decision Tree model
model_path = "decision.pkl"
with open(model_path, "rb") as f:
  model = pickle.load(f)

# HTML template with modern styling (Tailwind CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Placement Predictor</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-indigo-50 to-blue-100 min-h-screen py-10 px-4">
    <div class="max-w-3xl mx-auto bg-white shadow-xl rounded-2xl p-8">
        <div class="text-center mb-8">
            <h1 class="text-3xl font-extrabold text-gray-800">Campus Placement Predictor</h1>
            <p class="text-gray-500 mt-2">Enter student academic and professional details to predict placement status.</p>
        </div>

        {% if prediction_text %}
        <div class="mb-8 p-4 rounded-xl text-center font-semibold text-lg shadow-md 
            {% if 'Placed' in prediction_text and 'Not' not in prediction_text %} bg-green-100 text-green-700 border border-green-300
            {% else %} bg-red-100 text-red-700 border border-red-300 {% endif %}">
            {{ prediction_text }}
        </div>
        {% endif %}

        <form action="/" method="POST" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Gender -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                <select name="gender" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                </select>
            </div>

            <!-- Work Experience -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Work Experience</label>
                <select name="workex" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
                    <option value="No">No</option>
                    <option value="Yes">Yes</option>
                </select>
            </div>

            <!-- SSC Percentage -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">10th Grade (SSC) %</label>
                <input type="number" step="0.01" name="ssc_p" placeholder="e.g. 67.0" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
            </div>

            <!-- SSC Board -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">10th Board (SSC)</label>
                <select name="ssc_b" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
                    <option value="Central">Central</option>
                    <option value="Others">Others</option>
                </select>
            </div>

            <!-- HSC Percentage -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">12th Grade (HSC) %</label>
                <input type="number" step="0.01" name="hsc_p" placeholder="e.g. 75.5" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
            </div>

            <!-- HSC Board -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">12th Board (HSC)</label>
                <select name="hsc_b" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
                    <option value="Central">Central</option>
                    <option value="Others">Others</option>
                </select>
            </div>

            <!-- HSC Stream -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">12th Stream (HSC)</label>
                <select name="hsc_s" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
                    <option value="Commerce">Commerce</option>
                    <option value="Science">Science</option>
                    <option value="Arts">Arts</option>
                </select>
            </div>

            <!-- Degree Percentage -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Degree %</label>
                <input type="number" step="0.01" name="degree_p" placeholder="e.g. 65.0" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
            </div>

            <!-- Degree Type -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Degree Type</label>
                <select name="degree_t" required class="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-indigo-500">
                    <option value="Comm&Mgmt">Comm&Mgmt</option>
                    <option value="Sci&Tech">Sci&Tech</option>
                    <option value="Others">Others</option
