"""
Demo of the new violinplot functionality
http://matplotlib.org/examples/statistics/violinplot_demo.html
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.boxplots import violinplot

# fake data
fs = 10 # fontsize
pos = [1,2,3,4,5]
# data = [np.random.normal(size=100) for i in pos]
data = [
    [0.466, 0.517, 0.469, 0.52, 0.451, 0.478, 0.52, 0.504, 0.523, 0.503, 0.494, 0.509, 0.522, 0.482, 0.459, 0.504, 0.498, 0.523, 0.499, 0.479, 0.519, 0.522, 0.45, 0.52, 0.513, 0.477, 0.514, 0.51, 0.519, 0.494, 0.485, 0.502, 0.52, 0.461, 0.472, 0.457, 0.481, 0.522, 0.471, 0.48, 0.457, 0.503, 0.472, 0.483, 0.483, 0.471, 0.507, 0.465, 0.504, 0.492, 0.519, 0.518, 0.518, 0.471, 0.479, 0.524, 0.471, 0.529, 0.506, 0.509, 0.465, 0.472, 0.528, 0.526, 0.512, 0.51, 0.476, 0.505, 0.511, 0.49, 0.507, 0.525, 0.493, 0.521, 0.468, 0.525, 0.502, 0.491, 0.521, 0.5, 0.485, 0.525, 0.464, 0.486, 0.48, 0.458, 0.495, 0.497, 0.508, 0.51, 0.517, 0.513, 0.517, 0.526, 0.483, 0.5, 0.508, 0.491, 0.49, 0.489, 0.498, 0.509, 0.477, 0.504, 0.514, 0.512, 0.484, 0.5, 0.492, 0.497, 0.416, 0.513, 0.521, 0.5, 0.501, 0.518, 0.486, 0.51, 0.491, 0.521, 0.511, 0.468, 0.473, 0.499, 0.513, 0.476, 0.493, 0.516, 0.515, 0.511, 0.491, 0.52, 0.493, 0.505, 0.509, 0.514, 0.509, 0.516, 0.513, 0.489, 0.491, 0.507, 0.512, 0.466, 0.447, 0.509, 0.481, 0.46, 0.506, 0.502, 0.48, 0.489, 0.507, 0.48, 0.51, 0.495, 0.519, 0.485, 0.503, 0.513, 0.496, 0.522, 0.511, 0.503, 0.489, 0.509, 0.488, 0.508, 0.472, 0.493, 0.515, 0.477, 0.503, 0.517, 0.465, 0.506, 0.517, 0.454, 0.515, 0.497, 0.49, 0.503, 0.483, 0.461, 0.523, 0.522, 0.49, 0.476, 0.518, 0.486, 0.473, 0.474, 0.512, 0.516, 0.487, 0.448, 0.5, 0.502, 0.461, 0.485, 0.472, 0.506, 0.507, 0.514, 0.493, 0.498, 0.464, 0.494, 0.516, 0.525, 0.474, 0.484, 0.523, 0.493, 0.51, 0.478, 0.479, 0.469, 0.512, 0.492, 0.521, 0.487, 0.484, 0.502, 0.509, 0.508, 0.482, 0.516, 0.472, 0.48, 0.457, 0.511, 0.457, 0.509, 0.472, 0.522, 0.487, 0.481, 0.516, 0.49, 0.496, 0.466, 0.481, 0.508, 0.498, 0.495, 0.501, 0.516, 0.481, 0.523],
    [0.469, 0.486, 0.501, 0.473, 0.512, 0.485, 0.497, 0.51, 0.507, 0.517, 0.503, 0.516, 0.49, 0.507, 0.513, 0.467, 0.51, 0.507, 0.439, 0.492, 0.515, 0.514, 0.493, 0.52, 0.508, 0.467, 0.483, 0.49, 0.479, 0.506, 0.483, 0.482, 0.48, 0.511, 0.518, 0.505, 0.515, 0.49, 0.48, 0.52, 0.503, 0.48, 0.507, 0.52, 0.507, 0.488, 0.518, 0.506, 0.477, 0.519, 0.495, 0.488, 0.495, 0.501, 0.495, 0.493, 0.518, 0.504, 0.513, 0.502, 0.473, 0.505, 0.491, 0.509, 0.505, 0.501, 0.508, 0.518, 0.512, 0.514, 0.504, 0.52, 0.508, 0.512, 0.514, 0.518, 0.505, 0.518, 0.501, 0.512, 0.509, 0.508, 0.498, 0.513, 0.492, 0.507, 0.497, 0.514, 0.511, 0.519, 0.52, 0.512, 0.502, 0.509, 0.51, 0.508, 0.504, 0.508, 0.514, 0.508, 0.507, 0.511, 0.518, 0.518, 0.517, 0.52, 0.518, 0.512, 0.522, 0.518, 0.513, 0.511, 0.522, 0.516, 0.522, 0.515, 0.522, 0.522, 0.519, 0.518, 0.524, 0.523, 0.519, 0.52, 0.512, 0.52, 0.525, 0.523, 0.521, 0.511, 0.518, 0.522, 0.526, 0.519, 0.522, 0.521, 0.518, 0.524, 0.519, 0.515, 0.516, 0.516, 0.526, 0.524, 0.515, 0.516, 0.52, 0.522, 0.524, 0.518, 0.512, 0.515, 0.51, 0.513, 0.523, 0.517, 0.505, 0.516, 0.518, 0.521, 0.528, 0.518, 0.529, 0.518, 0.524, 0.507, 0.521, 0.506, 0.526, 0.504, 0.511, 0.507, 0.509, 0.522, 0.526, 0.522, 0.522, 0.505, 0.519, 0.516, 0.521, 0.518, 0.521, 0.513, 0.524, 0.508, 0.529, 0.5, 0.515, 0.524, 0.515, 0.52, 0.52, 0.52, 0.515, 0.525, 0.526, 0.502, 0.522, 0.52, 0.421, 0.476, 0.501, 0.493, 0.483, 0.494, 0.522, 0.483, 0.502, 0.489, 0.483, 0.503, 0.503, 0.514, 0.518, 0.52, 0.52, 0.522, 0.497, 0.503, 0.525, 0.5, 0.506, 0.521, 0.529, 0.511, 0.487, 0.523, 0.51, 0.516, 0.519, 0.495, 0.523, 0.529, 0.521, 0.512, 0.487, 0.509, 0.486, 0.524, 0.509, 0.524, 0.496, 0.501, 0.52, 0.525, 0.436, 0.495, 0.515, 0.525],
    [0.49, 0.472, 0.473, 0.478, 0.48, 0.503, 0.463, 0.5, 0.498, 0.513, 0.513, 0.494, 0.48, 0.456, 0.516, 0.491, 0.459, 0.483, 0.493, 0.488, 0.507, 0.46, 0.504, 0.481, 0.515, 0.477, 0.502, 0.495, 0.473, 0.508, 0.499, 0.519, 0.486, 0.474, 0.474, 0.467, 0.509, 0.517, 0.478, 0.461, 0.522, 0.514, 0.505, 0.516, 0.516, 0.516, 0.514, 0.498, 0.505, 0.496, 0.473, 0.483, 0.434, 0.496, 0.511, 0.5, 0.509, 0.491, 0.496, 0.491, 0.497, 0.509, 0.509, 0.516, 0.505, 0.435, 0.45, 0.426, 0.516, 0.499, 0.513, 0.489, 0.508, 0.478, 0.513, 0.51, 0.496, 0.452, 0.517, 0.508, 0.503, 0.435, 0.498, 0.511, 0.501, 0.489, 0.508, 0.511, 0.448, 0.484, 0.488, 0.439, 0.511, 0.503, 0.513, 0.492, 0.499, 0.47, 0.512, 0.494, 0.519, 0.51, 0.513, 0.514, 0.52, 0.519, 0.511, 0.514, 0.508, 0.501, 0.519, 0.52, 0.514, 0.511, 0.525, 0.52, 0.52, 0.52, 0.51, 0.526, 0.522, 0.526, 0.514, 0.525, 0.516, 0.506, 0.522, 0.504, 0.509, 0.518, 0.515, 0.511, 0.514, 0.507, 0.521, 0.51, 0.513, 0.505, 0.522, 0.508, 0.521, 0.501, 0.522, 0.517, 0.519, 0.5, 0.525, 0.508, 0.519, 0.516, 0.518, 0.499, 0.51, 0.519, 0.515, 0.517, 0.513, 0.505, 0.513, 0.517, 0.52, 0.512, 0.515, 0.517, 0.529, 0.528, 0.521, 0.516, 0.525, 0.522, 0.517, 0.517, 0.515, 0.516, 0.52, 0.507, 0.522, 0.518, 0.514, 0.514, 0.522, 0.526, 0.521, 0.519, 0.522, 0.521, 0.523, 0.522, 0.513, 0.518, 0.522, 0.524, 0.511, 0.521, 0.529, 0.517, 0.514, 0.513, 0.518, 0.518, 0.513, 0.517, 0.517, 0.505, 0.483, 0.522, 0.478, 0.524, 0.498, 0.46, 0.52, 0.522, 0.488, 0.515, 0.505, 0.5, 0.481, 0.484, 0.52, 0.518, 0.522, 0.503, 0.516, 0.497, 0.518, 0.449, 0.522, 0.492, 0.51, 0.528, 0.523, 0.531, 0.521, 0.514, 0.522, 0.509, 0.513, 0.516, 0.515, 0.51, 0.516, 0.519, 0.478, 0.516, 0.5, 0.521, 0.495, 0.523, 0.521, 0.488],
    # [0.484, 0.484, 0.452, 0.498, 0.516, 0.465, 0.497, 0.481, 0.499, 0.47, 0.476, 0.514, 0.488, 0.51, 0.511, 0.493, 0.525, 0.464, 0.494, 0.488, 0.5, 0.494, 0.47, 0.516, 0.507, 0.5, 0.519, 0.484, 0.47, 0.475, 0.459, 0.514, 0.464, 0.5, 0.52, 0.5, 0.485, 0.473, 0.479, 0.496, 0.464, 0.496, 0.48, 0.506, 0.47, 0.472, 0.503, 0.514, 0.5, 0.474, 0.497, 0.512, 0.496, 0.47, 0.499, 0.504, 0.474, 0.463, 0.511, 0.515, 0.492, 0.497, 0.471, 0.514, 0.475, 0.513, 0.492, 0.514, 0.513, 0.515, 0.5, 0.516, 0.475, 0.508, 0.506, 0.478, 0.507, 0.5, 0.509, 0.491, 0.507, 0.475, 0.484, 0.509, 0.494, 0.497, 0.49, 0.516, 0.484, 0.498, 0.51, 0.509, 0.515, 0.511, 0.506, 0.493, 0.519, 0.517, 0.493, 0.513, 0.503, 0.511, 0.524, 0.501, 0.498, 0.522, 0.509, 0.517, 0.505, 0.524, 0.495, 0.51, 0.502, 0.503, 0.493, 0.507, 0.508, 0.52, 0.525, 0.512, 0.498, 0.509, 0.521, 0.519, 0.499, 0.519, 0.5, 0.511, 0.505, 0.521, 0.515, 0.518, 0.514, 0.52, 0.498, 0.522, 0.52, 0.51, 0.504, 0.522, 0.515, 0.521, 0.522, 0.515, 0.519, 0.52, 0.521, 0.52, 0.507, 0.518, 0.516, 0.493, 0.508, 0.48, 0.486, 0.484, 0.479, 0.488, 0.504, 0.495, 0.519, 0.518, 0.534, 0.525, 0.514, 0.525, 0.505, 0.504, 0.503, 0.478, 0.498, 0.485, 0.51, 0.508, 0.522, 0.526, 0.486, 0.481, 0.485, 0.522, 0.502, 0.513, 0.504, 0.516, 0.522, 0.524, 0.514, 0.521, 0.502, 0.512, 0.522, 0.522, 0.495, 0.522, 0.482, 0.499, 0.519, 0.501, 0.527, 0.528, 0.504, 0.486, 0.468, 0.498, 0.481, 0.533, 0.502, 0.516, 0.434, 0.474, 0.526, 0.514, 0.508, 0.518, 0.522, 0.533, 0.499, 0.523, 0.499, 0.515, 0.51, 0.518, 0.52, 0.521, 0.507, 0.523, 0.48, 0.467, 0.503, 0.489, 0.498, 0.515, 0.519, 0.477, 0.516, 0.516, 0.519, 0.477, 0.513, 0.503, 0.522, 0.497, 0.52, 0.466, 0.522, 0.493, 0.521, 0.525, 0.509, 0.521],
    # [0.493, 0.441, 0.483, 0.518, 0.511, 0.483, 0.496, 0.513, 0.513, 0.514, 0.496, 0.487, 0.495, 0.5, 0.511, 0.499, 0.478, 0.503, 0.486, 0.469, 0.516, 0.516, 0.511, 0.517, 0.513, 0.512, 0.509, 0.455, 0.499, 0.496, 0.501, 0.511, 0.516, 0.477, 0.514, 0.495, 0.504, 0.509, 0.483, 0.515, 0.521, 0.515, 0.482, 0.514, 0.512, 0.504, 0.517, 0.508, 0.501, 0.515, 0.463, 0.491, 0.494, 0.483, 0.488, 0.481, 0.469, 0.47, 0.514, 0.45, 0.456, 0.49, 0.509, 0.504, 0.513, 0.485, 0.506, 0.511, 0.495, 0.509, 0.493, 0.511, 0.455, 0.504, 0.481, 0.503, 0.494, 0.459, 0.485, 0.487, 0.503, 0.512, 0.509, 0.478, 0.508, 0.48, 0.513, 0.46, 0.473, 0.513, 0.484, 0.471, 0.507, 0.498, 0.479, 0.49, 0.505, 0.509, 0.513, 0.478, 0.518, 0.5, 0.484, 0.49, 0.498, 0.51, 0.489, 0.506, 0.515, 0.516, 0.492, 0.505, 0.498, 0.489, 0.52, 0.517, 0.483, 0.512, 0.502, 0.496, 0.496, 0.489, 0.511, 0.491, 0.516, 0.487, 0.514, 0.521, 0.518, 0.514, 0.516, 0.493, 0.492, 0.509, 0.518, 0.523, 0.498, 0.512, 0.517, 0.484, 0.509, 0.502, 0.511, 0.511, 0.49, 0.486, 0.525, 0.502, 0.52, 0.515, 0.48, 0.459, 0.498, 0.507, 0.521, 0.489, 0.522, 0.458, 0.518, 0.5, 0.452, 0.49, 0.467, 0.5, 0.514, 0.493, 0.493, 0.517, 0.522, 0.482, 0.512, 0.522, 0.522, 0.528, 0.521, 0.509, 0.481, 0.511, 0.524, 0.455, 0.526, 0.453, 0.459, 0.486, 0.497, 0.458, 0.51, 0.487, 0.491, 0.532, 0.452, 0.526, 0.478, 0.517, 0.488, 0.524, 0.517, 0.488, 0.529, 0.473, 0.479, 0.473, 0.483, 0.523, 0.516, 0.491, 0.487, 0.521, 0.488, 0.481, 0.487, 0.532, 0.52, 0.493, 0.47, 0.503, 0.502, 0.53, 0.512, 0.498, 0.501, 0.504, 0.519, 0.503, 0.497, 0.492, 0.457, 0.487, 0.49, 0.524, 0.496, 0.463, 0.457, 0.49, 0.508, 0.504, 0.516, 0.496, 0.491, 0.506, 0.533, 0.491, 0.472, 0.475, 0.449, 0.533, 0.52, 0.518, 0.474, 0.509],
    # [0.487, 0.48, 0.512, 0.514, 0.48, 0.5, 0.517, 0.475, 0.483, 0.516, 0.465, 0.49, 0.489, 0.511, 0.497, 0.471, 0.513, 0.508, 0.479, 0.507, 0.516, 0.498, 0.476, 0.518, 0.476, 0.508, 0.504, 0.5, 0.481, 0.521, 0.487, 0.47, 0.516, 0.511, 0.48, 0.518, 0.494, 0.501, 0.507, 0.521, 0.485, 0.512, 0.484, 0.517, 0.518, 0.468, 0.461, 0.512, 0.516, 0.454, 0.444, 0.48, 0.501, 0.456, 0.481, 0.5, 0.448, 0.513, 0.479, 0.51, 0.504, 0.455, 0.488, 0.503, 0.485, 0.504, 0.456, 0.519, 0.488, 0.504, 0.514, 0.509, 0.489, 0.518, 0.477, 0.508, 0.514, 0.497, 0.505, 0.508, 0.499, 0.519, 0.511, 0.482, 0.506, 0.504, 0.511, 0.517, 0.51, 0.46, 0.502, 0.516, 0.497, 0.467, 0.499, 0.508, 0.494, 0.51, 0.512, 0.488, 0.492, 0.518, 0.503, 0.492, 0.506, 0.491, 0.507, 0.504, 0.498, 0.527, 0.526, 0.521, 0.519, 0.505, 0.512, 0.507, 0.519, 0.517, 0.528, 0.525, 0.505, 0.498, 0.492, 0.52, 0.504, 0.52, 0.515, 0.497, 0.504, 0.529, 0.521, 0.511, 0.482, 0.515, 0.52, 0.513, 0.499, 0.517, 0.51, 0.491, 0.522, 0.518, 0.524, 0.498, 0.519, 0.522, 0.517, 0.526, 0.512, 0.52, 0.504, 0.503, 0.479, 0.496, 0.465, 0.475, 0.506, 0.461, 0.504, 0.52, 0.508, 0.515, 0.462, 0.489, 0.498, 0.501, 0.496, 0.526, 0.509, 0.52, 0.502, 0.483, 0.528, 0.52, 0.523, 0.527, 0.486, 0.521, 0.492, 0.522, 0.521, 0.508, 0.521, 0.515, 0.522, 0.488, 0.51, 0.493, 0.516, 0.528, 0.519, 0.511, 0.49, 0.517, 0.488, 0.523, 0.523, 0.527, 0.529, 0.479, 0.512, 0.509, 0.501, 0.486, 0.491, 0.523, 0.507, 0.478, 0.47, 0.483, 0.503, 0.511, 0.508, 0.474, 0.449, 0.498, 0.51, 0.486, 0.476, 0.501, 0.474, 0.474, 0.52, 0.522, 0.514, 0.506, 0.513, 0.49, 0.519, 0.516, 0.492, 0.517, 0.475, 0.522, 0.515, 0.505, 0.467, 0.488, 0.508, 0.471, 0.515, 0.507, 0.527, 0.474, 0.486, 0.517, 0.513, 0.492, 0.518, 0.516],
    # [0.52, 0.475, 0.511, 0.495, 0.522, 0.512, 0.468, 0.51, 0.468, 0.523, 0.516, 0.517, 0.464, 0.496, 0.525, 0.469, 0.489, 0.479, 0.522, 0.511, 0.488, 0.495, 0.523, 0.453, 0.49, 0.473, 0.501, 0.494, 0.506, 0.458, 0.505, 0.477, 0.522, 0.512, 0.482, 0.489, 0.479, 0.515, 0.471, 0.518, 0.504, 0.478, 0.517, 0.491, 0.494, 0.504, 0.492, 0.499, 0.487, 0.468, 0.479, 0.519, 0.463, 0.511, 0.46, 0.478, 0.508, 0.477, 0.51, 0.457, 0.487, 0.503, 0.495, 0.47, 0.499, 0.497, 0.494, 0.503, 0.509, 0.51, 0.516, 0.516, 0.515, 0.514, 0.481, 0.511, 0.464, 0.495, 0.497, 0.51, 0.513, 0.485, 0.493, 0.513, 0.515, 0.465, 0.489, 0.512, 0.488, 0.502, 0.504, 0.512, 0.512, 0.466, 0.511, 0.515, 0.506, 0.493, 0.478, 0.465, 0.494, 0.502, 0.508, 0.515, 0.483, 0.504, 0.507, 0.525, 0.475, 0.521, 0.518, 0.508, 0.512, 0.503, 0.519, 0.481, 0.509, 0.497, 0.506, 0.514, 0.512, 0.483, 0.5, 0.519, 0.509, 0.519, 0.488, 0.513, 0.509, 0.502, 0.521, 0.513, 0.513, 0.51, 0.518, 0.516, 0.528, 0.516, 0.512, 0.519, 0.516, 0.513, 0.518, 0.508, 0.512, 0.522, 0.52, 0.498, 0.518, 0.491, 0.509, 0.489, 0.525, 0.522, 0.477, 0.519, 0.526, 0.509, 0.514, 0.489, 0.524, 0.503, 0.514, 0.482, 0.498, 0.489, 0.488, 0.504, 0.523, 0.507, 0.515, 0.521, 0.524, 0.503, 0.528, 0.493, 0.483, 0.523, 0.493, 0.517, 0.525, 0.47, 0.522, 0.51, 0.49, 0.521, 0.517, 0.514, 0.497, 0.473, 0.517, 0.517, 0.506, 0.523, 0.53, 0.519, 0.512, 0.527, 0.504, 0.525, 0.471, 0.49, 0.465, 0.469, 0.523, 0.524, 0.507, 0.529, 0.465, 0.534, 0.488, 0.525, 0.471, 0.533, 0.504, 0.522, 0.508, 0.513, 0.508, 0.503, 0.527, 0.537, 0.505, 0.527, 0.49, 0.523, 0.492, 0.526, 0.53, 0.497, 0.484, 0.485, 0.53, 0.522, 0.522, 0.536, 0.509, 0.494, 0.503, 0.537, 0.487, 0.52, 0.523, 0.514, 0.52, 0.472, 0.501, 0.487, 0.493, 0.531],
    [0.488, 0.467, 0.469, 0.502, 0.495, 0.461, 0.491, 0.477, 0.446, 0.507, 0.489, 0.497, 0.495, 0.502, 0.445, 0.502, 0.503, 0.491, 0.496, 0.473, 0.507, 0.503, 0.483, 0.515, 0.52, 0.491, 0.513, 0.509, 0.509, 0.511, 0.518, 0.504, 0.511, 0.489, 0.505, 0.516, 0.497, 0.507, 0.478, 0.512, 0.512, 0.517, 0.509, 0.498, 0.516, 0.465, 0.507, 0.502, 0.513, 0.515, 0.509, 0.477, 0.49, 0.418, 0.472, 0.474, 0.488, 0.486, 0.504, 0.484, 0.512, 0.493, 0.514, 0.479, 0.418, 0.496, 0.496, 0.481, 0.49, 0.518, 0.477, 0.491, 0.513, 0.515, 0.48, 0.52, 0.513, 0.475, 0.515, 0.483, 0.517, 0.519, 0.486, 0.484, 0.452, 0.484, 0.518, 0.508, 0.509, 0.497, 0.478, 0.51, 0.501, 0.515, 0.513, 0.506, 0.503, 0.515, 0.507, 0.474, 0.51, 0.514, 0.513, 0.511, 0.514, 0.52, 0.524, 0.52, 0.515, 0.511, 0.515, 0.522, 0.522, 0.512, 0.514, 0.519, 0.512, 0.523, 0.518, 0.521, 0.518, 0.523, 0.52, 0.517, 0.514, 0.518, 0.516, 0.517, 0.518, 0.521, 0.515, 0.517, 0.523, 0.518, 0.514, 0.527, 0.514, 0.517, 0.521, 0.522, 0.511, 0.518, 0.518, 0.519, 0.528, 0.514, 0.52, 0.509, 0.514, 0.513, 0.513, 0.516, 0.519, 0.517, 0.525, 0.524, 0.527, 0.519, 0.526, 0.526, 0.528, 0.527, 0.526, 0.516, 0.525, 0.514, 0.532, 0.519, 0.52, 0.523, 0.522, 0.524, 0.528, 0.514, 0.53, 0.525, 0.524, 0.523, 0.527, 0.522, 0.522, 0.521, 0.521, 0.523, 0.522, 0.525, 0.526, 0.518, 0.516, 0.516, 0.518, 0.525, 0.523, 0.523, 0.527, 0.518, 0.519, 0.522, 0.522, 0.521, 0.523, 0.499, 0.511, 0.522, 0.525, 0.517, 0.518, 0.517, 0.525, 0.525, 0.512, 0.508, 0.519, 0.521, 0.518, 0.526, 0.525, 0.519, 0.529, 0.513, 0.517, 0.528, 0.494, 0.512, 0.516, 0.516, 0.525, 0.515, 0.523, 0.523, 0.51, 0.519, 0.522, 0.531, 0.528, 0.527, 0.523, 0.523, 0.519, 0.526, 0.523, 0.51, 0.517, 0.522, 0.523, 0.529, 0.522, 0.497, 0.524, 0.522],
    [0.501, 0.462, 0.512, 0.515, 0.477, 0.443, 0.492, 0.466, 0.515, 0.504, 0.493, 0.508, 0.497, 0.49, 0.487, 0.513, 0.48, 0.514, 0.511, 0.434, 0.473, 0.517, 0.476, 0.481, 0.514, 0.471, 0.521, 0.518, 0.502, 0.467, 0.514, 0.493, 0.504, 0.505, 0.507, 0.515, 0.499, 0.505, 0.517, 0.51, 0.513, 0.512, 0.521, 0.513, 0.491, 0.505, 0.51, 0.486, 0.495, 0.494, 0.466, 0.488, 0.511, 0.486, 0.463, 0.473, 0.492, 0.506, 0.504, 0.514, 0.464, 0.514, 0.512, 0.465, 0.514, 0.492, 0.511, 0.5, 0.512, 0.52, 0.511, 0.507, 0.468, 0.51, 0.51, 0.49, 0.494, 0.439, 0.515, 0.519, 0.518, 0.507, 0.495, 0.473, 0.476, 0.513, 0.516, 0.489, 0.479, 0.499, 0.515, 0.518, 0.487, 0.517, 0.501, 0.51, 0.457, 0.513, 0.514, 0.503, 0.489, 0.512, 0.501, 0.504, 0.508, 0.511, 0.485, 0.507, 0.519, 0.511, 0.509, 0.486, 0.528, 0.494, 0.501, 0.506, 0.503, 0.512, 0.507, 0.519, 0.492, 0.507, 0.517, 0.487, 0.496, 0.508, 0.501, 0.513, 0.514, 0.518, 0.521, 0.517, 0.52, 0.518, 0.485, 0.515, 0.5, 0.491, 0.522, 0.497, 0.527, 0.52, 0.507, 0.51, 0.501, 0.518, 0.511, 0.521, 0.517, 0.495, 0.521, 0.485, 0.516, 0.526, 0.528, 0.517, 0.53, 0.515, 0.479, 0.505, 0.489, 0.524, 0.519, 0.518, 0.514, 0.525, 0.529, 0.519, 0.531, 0.502, 0.521, 0.525, 0.521, 0.52, 0.528, 0.528, 0.493, 0.521, 0.516, 0.489, 0.492, 0.507, 0.522, 0.522, 0.519, 0.524, 0.529, 0.523, 0.517, 0.53, 0.525, 0.523, 0.489, 0.516, 0.523, 0.513, 0.523, 0.513, 0.517, 0.512, 0.444, 0.516, 0.513, 0.497, 0.507, 0.501, 0.491, 0.51, 0.531, 0.492, 0.504, 0.482, 0.459, 0.524, 0.511, 0.505, 0.517, 0.52, 0.514, 0.525, 0.518, 0.527, 0.525, 0.511, 0.522, 0.525, 0.475, 0.518, 0.471, 0.523, 0.457, 0.524, 0.526, 0.493, 0.491, 0.505, 0.524, 0.525, 0.491, 0.473, 0.524, 0.523, 0.467, 0.524, 0.529, 0.514, 0.523, 0.477, 0.497, 0.5],
    # [0.462, 0.469, 0.468, 0.493, 0.51, 0.462, 0.517, 0.505, 0.512, 0.508, 0.508, 0.488, 0.476, 0.491, 0.492, 0.473, 0.513, 0.47, 0.516, 0.515, 0.469, 0.51, 0.515, 0.494, 0.516, 0.503, 0.518, 0.497, 0.502, 0.511, 0.506, 0.465, 0.518, 0.478, 0.515, 0.517, 0.489, 0.499, 0.516, 0.465, 0.49, 0.492, 0.512, 0.513, 0.491, 0.508, 0.491, 0.513, 0.499, 0.502, 0.506, 0.475, 0.483, 0.512, 0.512, 0.468, 0.511, 0.504, 0.511, 0.496, 0.487, 0.494, 0.506, 0.507, 0.511, 0.515, 0.473, 0.497, 0.507, 0.499, 0.491, 0.501, 0.506, 0.48, 0.44, 0.486, 0.489, 0.479, 0.511, 0.472, 0.489, 0.484, 0.511, 0.511, 0.494, 0.463, 0.467, 0.512, 0.515, 0.481, 0.504, 0.512, 0.514, 0.512, 0.513, 0.512, 0.516, 0.513, 0.513, 0.5, 0.511, 0.502, 0.511, 0.498, 0.509, 0.503, 0.497, 0.489, 0.515, 0.485, 0.524, 0.487, 0.495, 0.501, 0.511, 0.516, 0.488, 0.517, 0.485, 0.52, 0.486, 0.502, 0.489, 0.481, 0.497, 0.496, 0.486, 0.49, 0.495, 0.495, 0.507, 0.5, 0.494, 0.504, 0.518, 0.524, 0.504, 0.497, 0.518, 0.516, 0.499, 0.506, 0.495, 0.503, 0.486, 0.487, 0.492, 0.519, 0.51, 0.516, 0.487, 0.499, 0.522, 0.483, 0.5, 0.516, 0.5, 0.495, 0.524, 0.512, 0.515, 0.521, 0.502, 0.511, 0.525, 0.518, 0.518, 0.511, 0.529, 0.532, 0.488, 0.521, 0.514, 0.528, 0.517, 0.493, 0.506, 0.531, 0.525, 0.486, 0.51, 0.497, 0.496, 0.53, 0.502, 0.495, 0.514, 0.491, 0.529, 0.522, 0.498, 0.5, 0.504, 0.521, 0.511, 0.518, 0.519, 0.492, 0.524, 0.51, 0.451, 0.414, 0.502, 0.503, 0.447, 0.508, 0.522, 0.488, 0.506, 0.477, 0.518, 0.522, 0.524, 0.515, 0.518, 0.492, 0.502, 0.512, 0.495, 0.457, 0.401, 0.516, 0.497, 0.514, 0.489, 0.405, 0.507, 0.512, 0.519, 0.51, 0.527, 0.52, 0.493, 0.52, 0.507, 0.518, 0.518, 0.493, 0.525, 0.499, 0.521, 0.492, 0.482, 0.468, 0.504, 0.523, 0.498, 0.493, 0.519, 0.512],
]

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6,6))

# axes.violinplot(data, pos, points=20, widths=0.1,
#                       showmeans=True, showextrema=True, showmedians=True)
# axes.set_title('Custom violinplot 1', fontsize=fs)

# axes.violinplot(data, pos, points=40, widths=0.3,
#                       showmeans=True, showextrema=True, showmedians=True,
#                       bw_method='silverman')
# axes.set_title('Custom violinplot 2', fontsize=fs)

axes.violinplot(data, pos, points=250, widths=0.5, showmeans=True,
                      showextrema=True, showmedians=True, bw_method='silverman')
axes.set_title('Violinplots', fontsize=fs)

fig.suptitle("Violin Plotting")
fig.subplots_adjust(hspace=0.4)
plt.show()
