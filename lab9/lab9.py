import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import numpy as np

# Configurații pentru grafice
az.style.use("arviz-darkgrid")

# Datele problemei
y_values = [0, 5, 10]
theta_values = [0.2, 0.5]
combinations = [(y, t) for y in y_values for t in theta_values]

# Dicționar pentru a stoca rezultatele (trace-urile)
traces = {}

print("Se rulează eșantionarea pentru toate scenariile...")

for Y_obs, theta in combinations:
    key = f"Y={Y_obs}, θ={theta}"
    print(f"\nProcesare scenariu: {key}")
    
    with pm.Model() as model:
        # 1. Prior: n ~ Poisson(10)
        # Avem grijă ca n să fie cel puțin egal cu Y_obs. 
        # Deși Poisson are suport pe [0, inf), observațiile vor constrânge posteriorul.
        # Setăm initval pentru a evita erori de start (n < Y).
        n = pm.Poisson("n", mu=10, initval=max(10, Y_obs + 5))
        
        # 2. Likelihood: Y ~ Binomial(n, theta)
        # Observația Y_obs constrânge n (dacă n < Y_obs, probabilitatea este 0)
        obs = pm.Binomial("obs", n=n, p=theta, observed=Y_obs)
        
        # 3. Inferență (Posterior)
        # Folosim return_inferencedata=True pentru compatibilitate cu Arviz
        trace = pm.sample(draws=2000, tune=1000, chains=2, progressbar=False)
        
        # 4. Posterior Predictive (pentru punctul c)
        # Generăm un nou Y* (future_obs) bazat pe distribuția posterioară a lui n
        pp = pm.sample_posterior_predictive(trace, extend_inferencedata=True, progressbar=False)
        
        traces[key] = trace

# --- Vizualizare Punctul a) Posteriorul lui n ---
fig, axes = plt.subplots(3, 2, figsize=(12, 12), constrained_layout=True)
fig.suptitle("Punctul a) Distribuția Posterioară pentru n", fontsize=16)

axes = axes.flatten()
for i, (key, trace) in enumerate(traces.items()):
    az.plot_posterior(
        trace, 
        var_names=["n"], 
        ax=axes[i], 
        hdi_prob=0.94,
        textsize=12
    )
    axes[i].set_title(key)

plt.savefig("posterior_n.png")
print("\nGraficul pentru punctul a) a fost salvat ca 'posterior_n.png'")

# --- Vizualizare Punctul c) Posterior Predictive pentru Y* ---
fig2, axes2 = plt.subplots(3, 2, figsize=(12, 12), constrained_layout=True)
fig2.suptitle("Punctul c) Posterior Predictive pentru Y* (viitori cumpărători)", fontsize=16)

axes2 = axes2.flatten()
for i, (key, trace) in enumerate(traces.items()):
    # Accesăm datele predictive
    # Structura este trace.posterior_predictive["obs"]
    az.plot_dist(
        trace.posterior_predictive["obs"],
        ax=axes2[i],
        color="orange",
        label="Y* (Predictive)"
    )
    axes2[i].set_title(key)
    axes2[i].legend()
    axes2[i].set_xlabel("Nr. cumpărători (Y*)")

plt.savefig("posterior_predictive_y.png")
print("Graficul pentru punctul c) a fost salvat ca 'posterior_predictive_y.png'")

plt.show()