# PROJECT STRUCTURE

## LAYERS

The project has hierarchical order:
```
QLab/
│
├── core/
│   ├── system.py        
│   ├── hamiltonian.py   
│   ├── solver.py        
│   ├── photonics.py     
│   └── quantum.py       
│
├── optimization/
│   ├── base.py          
│   ├── genetic.py       
│   ├── multiobjective.py
│   ├── reinforcement.py
│   └── surrogate.py
│
├── visualization/
│   ├── bloch.py         
│   ├── fields.py        
│   └── optimization.py  
│
├── workflow/
│   ├── pipeline.py      
│   └── experiment.py    
│
└── utils/
    ├── io.py
    ├── math.py
    └── constants.py
```

Structure may vary across the time, changes will be documented here. If you want to see a previous version, check the commits on `dev` or `main` branch.


