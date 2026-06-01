from flask import Flask, render_template, request, jsonify
import random
import math
import copy
import time

app = Flask(__name__)

# ─── DATABASE MAKANAN ────────────────────────────────────────────────────────
FOOD_DATABASE = {
    # Sarapan
    "Nasi Putih (1 porsi)":      {"kalori": 206, "protein": 4.3, "lemak": 0.4, "karbo": 44.5, "serat": 0.6, "harga": 3000,  "waktu": ["sarapan","makan_siang","makan_malam"]},
    "Roti Gandum (2 lembar)":    {"kalori": 160, "protein": 6.0, "lemak": 2.0, "karbo": 30.0, "serat": 4.0, "harga": 5000,  "waktu": ["sarapan"]},
    "Oatmeal (1 porsi)":         {"kalori": 150, "protein": 5.0, "lemak": 3.0, "karbo": 27.0, "serat": 4.0, "harga": 8000,  "waktu": ["sarapan"]},
    "Telur Dadar (2 butir)":     {"kalori": 185, "protein": 13.0,"lemak": 14.0,"karbo": 1.0,  "serat": 0.0, "harga": 6000,  "waktu": ["sarapan","makan_siang"]},
    "Telur Rebus (2 butir)":     {"kalori": 155, "protein": 13.0,"lemak": 11.0,"karbo": 1.1,  "serat": 0.0, "harga": 5000,  "waktu": ["sarapan","makan_siang"]},
    "Susu Sapi (1 gelas)":       {"kalori": 150, "protein": 8.0, "lemak": 8.0, "karbo": 12.0, "serat": 0.0, "harga": 6000,  "waktu": ["sarapan","snack"]},
    "Yogurt (1 cup)":            {"kalori": 100, "protein": 17.0,"lemak": 0.7, "karbo": 6.0,  "serat": 0.0, "harga": 12000, "waktu": ["sarapan","snack"]},
    "Pisang (1 buah)":           {"kalori": 89,  "protein": 1.1, "lemak": 0.3, "karbo": 23.0, "serat": 2.6, "harga": 3000,  "waktu": ["sarapan","snack"]},
    "Alpukat (1/2 buah)":        {"kalori": 120, "protein": 1.5, "lemak": 11.0,"karbo": 6.0,  "serat": 5.0, "harga": 8000,  "waktu": ["sarapan","snack"]},
    # Makan siang / malam
    "Ayam Goreng (1 potong)":    {"kalori": 295, "protein": 32.0,"lemak": 17.0,"karbo": 3.0,  "serat": 0.2, "harga": 15000, "waktu": ["makan_siang","makan_malam"]},
    "Ayam Bakar (1 potong)":     {"kalori": 220, "protein": 30.0,"lemak": 10.0,"karbo": 2.0,  "serat": 0.0, "harga": 18000, "waktu": ["makan_siang","makan_malam"]},
    "Ikan Goreng (1 ekor)":      {"kalori": 210, "protein": 28.0,"lemak": 11.0,"karbo": 2.0,  "serat": 0.0, "harga": 12000, "waktu": ["makan_siang","makan_malam"]},
    "Ikan Bakar (1 ekor)":       {"kalori": 175, "protein": 27.0,"lemak": 7.0, "karbo": 1.0,  "serat": 0.0, "harga": 15000, "waktu": ["makan_siang","makan_malam"]},
    "Tempe Goreng (2 potong)":   {"kalori": 160, "protein": 11.0,"lemak": 9.0, "karbo": 10.0, "serat": 3.0, "harga": 4000,  "waktu": ["makan_siang","makan_malam"]},
    "Tahu Goreng (2 potong)":    {"kalori": 120, "protein": 9.0, "lemak": 7.0, "karbo": 4.0,  "serat": 0.5, "harga": 3000,  "waktu": ["makan_siang","makan_malam"]},
    "Sayur Bayam":               {"kalori": 45,  "protein": 3.5, "lemak": 0.5, "karbo": 7.0,  "serat": 2.5, "harga": 5000,  "waktu": ["makan_siang","makan_malam"]},
    "Sayur Kangkung":            {"kalori": 35,  "protein": 3.0, "lemak": 0.3, "karbo": 6.0,  "serat": 2.0, "harga": 5000,  "waktu": ["makan_siang","makan_malam"]},
    "Gado-Gado":                 {"kalori": 310, "protein": 13.0,"lemak": 20.0,"karbo": 22.0, "serat": 5.0, "harga": 15000, "waktu": ["makan_siang","makan_malam"]},
    "Soto Ayam":                 {"kalori": 250, "protein": 20.0,"lemak": 12.0,"karbo": 18.0, "serat": 1.5, "harga": 15000, "waktu": ["makan_siang","makan_malam"]},
    "Rendang (1 potong)":        {"kalori": 370, "protein": 28.0,"lemak": 26.0,"karbo": 6.0,  "serat": 1.0, "harga": 25000, "waktu": ["makan_siang","makan_malam"]},
    "Sup Tahu Sayur":            {"kalori": 120, "protein": 8.0, "lemak": 5.0, "karbo": 12.0, "serat": 3.0, "harga": 10000, "waktu": ["makan_siang","makan_malam"]},
    # Snack
    "Apel (1 buah)":             {"kalori": 95,  "protein": 0.5, "lemak": 0.3, "karbo": 25.0, "serat": 4.4, "harga": 5000,  "waktu": ["snack"]},
    "Jeruk (1 buah)":            {"kalori": 62,  "protein": 1.2, "lemak": 0.2, "karbo": 15.0, "serat": 3.1, "harga": 4000,  "waktu": ["snack"]},
    "Kacang Almond (30g)":       {"kalori": 173, "protein": 6.0, "lemak": 15.0,"karbo": 6.0,  "serat": 3.5, "harga": 10000, "waktu": ["snack"]},
    "Biskuit Gandum (4 keping)": {"kalori": 120, "protein": 3.0, "lemak": 4.0, "karbo": 20.0, "serat": 2.0, "harga": 5000,  "waktu": ["snack"]},
}

FOOD_NAMES = list(FOOD_DATABASE.keys())

# ─── TARGET NUTRISI BERDASARKAN PROFIL ────────────────────────────────────────
def get_nutrition_target(berat, tinggi, usia, gender, aktivitas):
    # BMR - Harris-Benedict
    if gender == "pria":
        bmr = 88.362 + (13.397 * berat) + (4.799 * tinggi) - (5.677 * usia)
    else:
        bmr = 447.593 + (9.247 * berat) + (3.098 * tinggi) - (4.330 * usia)
    
    faktor = {"sedentary":1.2, "ringan":1.375, "sedang":1.55, "berat":1.725, "sangat_berat":1.9}
    tdee = bmr * faktor.get(aktivitas, 1.55)
    
    return {
        "kalori":  round(tdee),
        "protein": round(berat * 1.6),       # 1.6g/kg BB
        "lemak":   round(tdee * 0.25 / 9),   # 25% dari kalori
        "karbo":   round(tdee * 0.50 / 4),   # 50% dari kalori
        "serat":   25,                         # AKG 25g
    }

# ─── MEAL SLOTS ──────────────────────────────────────────────────────────────
MEAL_SLOTS = ["sarapan", "snack_pagi", "makan_siang", "snack_sore", "makan_malam"]
SLOT_WAKTU = {
    "sarapan":    "sarapan",
    "snack_pagi": "snack",
    "makan_siang":"makan_siang",
    "snack_sore": "snack",
    "makan_malam":"makan_malam",
}
SLOT_RATIO = {  # proporsi kalori tiap slot
    "sarapan":    0.25,
    "snack_pagi": 0.10,
    "makan_siang":0.35,
    "snack_sore": 0.10,
    "makan_malam":0.20,
}

def get_candidates(slot):
    waktu = SLOT_WAKTU[slot]
    return [f for f, d in FOOD_DATABASE.items() if waktu in d["waktu"]]

def random_menu():
    """Generate menu acak: dict {slot: [makanan1, makanan2]}"""
    menu = {}
    for slot in MEAL_SLOTS:
        cands = get_candidates(slot)
        n = 2 if "snack" in slot else 3
        menu[slot] = random.sample(cands, min(n, len(cands)))
    return menu

def calc_nutrition(menu):
    total = {"kalori":0,"protein":0,"lemak":0,"karbo":0,"serat":0,"harga":0}
    for slot, foods in menu.items():
        for f in foods:
            for k in total:
                total[k] += FOOD_DATABASE[f].get(k, 0)
    return total

def fitness(menu, target, budget):
    nutr = calc_nutrition(menu)
    score = 0
    # Penalti deviasi nutrisi (makin kecil deviasi, makin baik)
    for k in ["kalori","protein","lemak","karbo","serat"]:
        dev = abs(nutr[k] - target[k]) / max(target[k], 1)
        score -= dev * 100
    # Penalti budget
    if nutr["harga"] > budget:
        score -= (nutr["harga"] - budget) / 1000 * 20
    # Bonus variasi (tidak ada makanan berulang)
    all_foods = [f for foods in menu.values() for f in foods]
    unique_ratio = len(set(all_foods)) / len(all_foods)
    score += unique_ratio * 10
    return score

def get_neighbor(menu):
    """Buat satu perubahan kecil pada menu"""
    new_menu = copy.deepcopy(menu)
    slot = random.choice(MEAL_SLOTS)
    idx = random.randint(0, len(new_menu[slot]) - 1)
    cands = get_candidates(slot)
    current = new_menu[slot][idx]
    alternatives = [f for f in cands if f not in new_menu[slot]]
    if alternatives:
        new_menu[slot][idx] = random.choice(alternatives)
    return new_menu

# ═══════════════════════════════════════════════════════════════════
# HILL CLIMBING
# ═══════════════════════════════════════════════════════════════════
def hill_climbing(target, budget, variant="steepest", max_iter=300):
    start = time.time()
    current = random_menu()
    current_fit = fitness(current, target, budget)
    history = [{"iter":0, "fitness": round(current_fit,3), "kalori": calc_nutrition(current)["kalori"]}]
    
    for i in range(1, max_iter+1):
        if variant == "steepest":
            neighbors = [get_neighbor(current) for _ in range(8)]
            fits = [(fitness(n, target, budget), n) for n in neighbors]
            best_fit, best_n = max(fits, key=lambda x: x[0])
            if best_fit > current_fit:
                current, current_fit = best_n, best_fit
            else:
                break
        elif variant == "stochastic":
            neighbor = get_neighbor(current)
            nf = fitness(neighbor, target, budget)
            if nf > current_fit:
                current, current_fit = neighbor, nf
        else:  # simple
            neighbor = get_neighbor(current)
            nf = fitness(neighbor, target, budget)
            if nf > current_fit:
                current, current_fit = neighbor, nf
                history.append({"iter":i,"fitness":round(current_fit,3),"kalori":calc_nutrition(current)["kalori"]})
                continue
            else:
                break
        
        if i % 10 == 0 or i <= 5:
            history.append({"iter":i,"fitness":round(current_fit,3),"kalori":calc_nutrition(current)["kalori"]})
    
    elapsed = round((time.time()-start)*1000, 1)
    return {
        "menu": current,
        "nutrition": calc_nutrition(current),
        "fitness": round(current_fit, 3),
        "history": history,
        "iterations": i,
        "time_ms": elapsed,
        "algorithm": f"Hill Climbing ({variant.title()})"
    }

# ═══════════════════════════════════════════════════════════════════
# SIMULATED ANNEALING
# ═══════════════════════════════════════════════════════════════════
def simulated_annealing(target, budget, T0=100, cooling=0.97, T_min=0.1):
    start = time.time()
    current = random_menu()
    current_fit = fitness(current, target, budget)
    best = copy.deepcopy(current)
    best_fit = current_fit
    T = T0
    history = [{"iter":0,"fitness":round(best_fit,3),"temperature":round(T,2),"kalori":calc_nutrition(current)["kalori"]}]
    i = 0
    accepted_worse = 0
    
    while T > T_min:
        i += 1
        neighbor = get_neighbor(current)
        nf = fitness(neighbor, target, budget)
        dE = nf - current_fit
        
        if dE > 0:
            current, current_fit = neighbor, nf
        else:
            prob = math.exp(dE / T)
            if random.random() < prob:
                current, current_fit = neighbor, nf
                accepted_worse += 1
        
        if current_fit > best_fit:
            best = copy.deepcopy(current)
            best_fit = current_fit
        
        T *= cooling
        if i % 20 == 0:
            history.append({"iter":i,"fitness":round(best_fit,3),"temperature":round(T,2),"kalori":calc_nutrition(best)["kalori"]})
    
    elapsed = round((time.time()-start)*1000, 1)
    return {
        "menu": best,
        "nutrition": calc_nutrition(best),
        "fitness": round(best_fit, 3),
        "history": history,
        "iterations": i,
        "accepted_worse": accepted_worse,
        "time_ms": elapsed,
        "algorithm": "Simulated Annealing"
    }

# ═══════════════════════════════════════════════════════════════════
# GENETIC ALGORITHM
# ═══════════════════════════════════════════════════════════════════
def tournament_select(pop, fits, k=3):
    idxs = random.sample(range(len(pop)), k)
    best_idx = max(idxs, key=lambda i: fits[i])
    return copy.deepcopy(pop[best_idx])

def crossover(p1, p2):
    child = {}
    for slot in MEAL_SLOTS:
        if random.random() < 0.5:
            child[slot] = copy.copy(p1[slot])
        else:
            child[slot] = copy.copy(p2[slot])
    return child

def mutate(menu, prob=0.15):
    new_menu = copy.deepcopy(menu)
    for slot in MEAL_SLOTS:
        if random.random() < prob:
            cands = get_candidates(slot)
            idx = random.randint(0, len(new_menu[slot])-1)
            alternatives = [f for f in cands if f not in new_menu[slot]]
            if alternatives:
                new_menu[slot][idx] = random.choice(alternatives)
    return new_menu

def genetic_algorithm(target, budget, pop_size=30, max_gen=100, cx_prob=0.8, mut_prob=0.15, elitism=3):
    start = time.time()
    population = [random_menu() for _ in range(pop_size)]
    history = []
    
    for gen in range(max_gen):
        fits = [fitness(ind, target, budget) for ind in population]
        sorted_pop = sorted(zip(fits, population), key=lambda x: x[0], reverse=True)
        best_fit = sorted_pop[0][0]
        avg_fit = sum(fits) / len(fits)
        
        if gen % 5 == 0:
            history.append({
                "gen": gen,
                "best_fitness": round(best_fit, 3),
                "avg_fitness": round(avg_fit, 3),
                "kalori": calc_nutrition(sorted_pop[0][1])["kalori"]
            })
        
        # Elitisme
        new_pop = [copy.deepcopy(ind) for _, ind in sorted_pop[:elitism]]
        
        while len(new_pop) < pop_size:
            p1 = tournament_select(population, fits)
            if random.random() < cx_prob:
                p2 = tournament_select(population, fits)
                child = crossover(p1, p2)
            else:
                child = copy.deepcopy(p1)
            child = mutate(child, mut_prob)
            new_pop.append(child)
        
        population = new_pop
    
    fits = [fitness(ind, target, budget) for ind in population]
    best_idx = max(range(len(fits)), key=lambda i: fits[i])
    best = population[best_idx]
    
    elapsed = round((time.time()-start)*1000, 1)
    return {
        "menu": best,
        "nutrition": calc_nutrition(best),
        "fitness": round(fits[best_idx], 3),
        "history": history,
        "generations": max_gen,
        "time_ms": elapsed,
        "algorithm": "Genetic Algorithm"
    }

# ─── ROUTES ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/foods")
def api_foods():
    return jsonify(FOOD_DATABASE)

@app.route("/api/optimize", methods=["POST"])
def api_optimize():
    data = request.json
    target = get_nutrition_target(
        berat=data.get("berat", 65),
        tinggi=data.get("tinggi", 165),
        usia=data.get("usia", 25),
        gender=data.get("gender", "pria"),
        aktivitas=data.get("aktivitas", "sedang")
    )
    budget = data.get("budget", 80000)
    algorithm = data.get("algorithm", "ga")
    
    if algorithm == "hc":
        variant = data.get("hc_variant", "steepest")
        result = hill_climbing(target, budget, variant=variant, max_iter=data.get("max_iter", 300))
    elif algorithm == "sa":
        result = simulated_annealing(
            target, budget,
            T0=data.get("T0", 100),
            cooling=data.get("cooling", 0.97),
            T_min=data.get("T_min", 0.1)
        )
    else:
        result = genetic_algorithm(
            target, budget,
            pop_size=data.get("pop_size", 30),
            max_gen=data.get("max_gen", 100),
            cx_prob=data.get("cx_prob", 0.8),
            mut_prob=data.get("mut_prob", 0.15),
            elitism=data.get("elitism", 3)
        )
    
    result["target"] = target
    result["budget"] = budget
    
    # Serialize menu dengan info nutrisi per item
    menu_detail = {}
    for slot, foods in result["menu"].items():
        menu_detail[slot] = [{"nama": f, **FOOD_DATABASE[f]} for f in foods]
    result["menu_detail"] = menu_detail
    del result["menu"]
    
    return jsonify(result)

@app.route("/api/compare", methods=["POST"])
def api_compare():
    data = request.json
    target = get_nutrition_target(
        berat=data.get("berat", 65), tinggi=data.get("tinggi", 165),
        usia=data.get("usia", 25), gender=data.get("gender", "pria"),
        aktivitas=data.get("aktivitas", "sedang")
    )
    budget = data.get("budget", 80000)
    
    hc_res  = hill_climbing(target, budget, variant="steepest", max_iter=300)
    sa_res  = simulated_annealing(target, budget)
    ga_res  = genetic_algorithm(target, budget, pop_size=25, max_gen=80)
    
    return jsonify({
        "target": target,
        "hc":  {"fitness": hc_res["fitness"],  "nutrition": hc_res["nutrition"],  "time_ms": hc_res["time_ms"],  "iterations": hc_res.get("iterations",0),  "history": hc_res["history"]},
        "sa":  {"fitness": sa_res["fitness"],  "nutrition": sa_res["nutrition"],  "time_ms": sa_res["time_ms"],  "iterations": sa_res.get("iterations",0),  "history": sa_res["history"]},
        "ga":  {"fitness": ga_res["fitness"],  "nutrition": ga_res["nutrition"],  "time_ms": ga_res["time_ms"],  "generations": ga_res.get("generations",0),"history": ga_res["history"]},
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug, host="0.0.0.0", port=port)
