"""
SIN HUMO - Control de Ahorros por Dejar de Fumar
App de escritorio para Windows con Python + tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import math
from datetime import datetime, date

APP_NAME = "SIN HUMO - Control de Ahorros"
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".sinhumo_config.json")
ICON_PATH = os.path.join(os.path.dirname(__file__), "sinhumo.ico")

COLORS = {
    "bg":           "#0f0f1a",
    "card":         "#1a1a2e",
    "card2":        "#16213e",
    "accent":       "#0f3460",
    "green":        "#00c896",
    "light_green":  "#55efc4",
    "text":         "#e8e8f0",
    "subtext":      "#8888aa",
    "yellow":       "#ffd166",
    "orange":       "#f4845f",
    "red":          "#ef476f",
    "blue":         "#118ab2",
    "border":       "#2a2a45",
}

MOTIVATIONAL_ITEMS = [
    (3,    "☕  Un café con leche",             "¡Pequeños placeres diarios!"),
    (5,    "🥐  Un café y un croissant",         "¡El desayuno perfecto!"),
    (8,    "🍺  Una cerveza con pinchos",         "¡A celebrar la salud!"),
    (10,   "📚  Un libro",                       "¡Invierte en ti mismo!"),
    (12,   "🎬  Una entrada de cine",             "¡Mereces entretenerte!"),
    (15,   "🍕  Una pizza con amigos",            "¡Comparte sin humo!"),
    (20,   "🎮  Un DLC o juego digital",          "¡Tiempo de ocio!"),
    (25,   "🍽️  Una cena en restaurante",         "¡Date el capricho!"),
    (30,   "👕  Una camiseta nueva",              "¡Renueva el armario!"),
    (40,   "🎁  Un regalo especial",              "¡Para ti o para quien quieras!"),
    (50,   "👖  Un pantalón o vaqueros",          "¡Te lo has ganado!"),
    (60,   "👟  Unas zapatillas de deporte",      "¡Para correr más sano!"),
    (75,   "🎧  Unos cascos inalámbricos",        "¡Música para el alma!"),
    (90,   "🧥  Un jersey de calidad",            "¡Estilo y calidez!"),
    (100,  "🎒  Una mochila resistente",          "¡Aventuras por delante!"),
    (130,  "🔊  Un altavoz Bluetooth",            "¡Música en todas partes!"),
    (150,  "🍳  Una freidora de aire",            "¡Cocina más sano!"),
    (200,  "⌚  Un smartwatch fitness",           "¡Cuida tu salud al detalle!"),
    (250,  "📷  Una cámara compacta",             "¡Captura tus momentos!"),
    (300,  "🏕️  Un fin de semana rural",          "¡Desconecta y recarga!"),
    (400,  "🚲  Una bicicleta",                   "¡Muévete más sano!"),
    (500,  "📱  Un smartphone nuevo",             "¡Conectado al mundo!"),
    (600,  "✈️  Un vuelo a Europa",               "¡El mundo te espera!"),
    (800,  "🎸  Una guitarra o instrumento",      "¡Aprende algo nuevo!"),
    (1000, "💻  Un portátil",                     "¡Invierte en tecnología!"),
    (1500, "🏖️  Una semana de vacaciones",        "¡Merecido descanso!"),
    (2000, "🚴  Una bici eléctrica",              "¡La libertad en dos ruedas!"),
    (3000, "🌍  Un viaje largo",                  "¡Explora el mundo!"),
    (5000, "🏍️  Una moto nueva",                  "¡La libertad te llama!"),
]

MOTIVATIONAL_QUOTES = [
    "Cada día sin fumar es una victoria que tu cuerpo agradece para siempre.",
    "El dinero que no gastas en tabaco es dinero que gastas en vivir.",
    "Llevas {days} días eligiendo la salud. ¡Eso es de campeones!",
    "Tu futuro yo te está agradeciendo cada cigarrillo que no enciendes.",
    "Más dinero, más salud, más vida. Así de simple.",
    "No lo llames sacrificio, llámalo inversión en ti mismo.",
    "Cada semana sin fumar es una semana que tu corazón late más fuerte.",
    "Ya has demostrado que puedes. Sigue demostrándotelo cada día.",
]


class SinHumoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("860x720")
        self.root.minsize(700, 600)
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(True, True)

        if os.path.exists(ICON_PATH):
            try:
                self.root.iconbitmap(ICON_PATH)
            except Exception:
                pass

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TScrollbar",
                        background=COLORS["accent"],
                        troughcolor=COLORS["card"],
                        bordercolor=COLORS["bg"],
                        arrowcolor=COLORS["text"],
                        lightcolor=COLORS["accent"],
                        darkcolor=COLORS["accent"])

        self._quote_index = 0
        self.config = self._load_config()

        if not self.config:
            self._show_setup()
        else:
            self._show_main()

    # ── Persistence ──────────────────────────────────────────────────────────

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    # ── Calculations ─────────────────────────────────────────────────────────

    def _calc(self):
        quit_date = date.fromisoformat(self.config["quit_date"])
        today = date.today()
        days = max(0, (today - quit_date).days)
        cost = self.config["daily_cost"]

        week_day = today.weekday()        # 0=Mon … 6=Sun
        days_in_week = min(days, week_day + 1)
        days_in_month = min(days, today.day)

        return {
            "quit_date":    quit_date,
            "days":         days,
            "total":        days * cost,
            "daily":        cost,
            "this_week":    days_in_week * cost,
            "weekly":       7 * cost,
            "biweekly":     14 * cost,
            "this_month":   days_in_month * cost,
            "monthly":      30 * cost,
            "yearly":       365 * cost,
            "cigs_avoided": int(days * self.config.get("cigs_per_day", 20)),
            "minutes_won":  days * 11,
        }

    def _get_items_for(self, total):
        affordable = [x for x in MOTIVATIONAL_ITEMS if x[0] <= total]
        upcoming   = [x for x in MOTIVATIONAL_ITEMS if x[0] > total]
        best = affordable[-1] if affordable else None
        nxt  = upcoming[0]   if upcoming   else None
        return best, nxt

    # ── Setup screen ─────────────────────────────────────────────────────────

    def _show_setup(self):
        self._clear()
        root = self.root

        outer = tk.Frame(root, bg=COLORS["bg"])
        outer.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85)

        tk.Label(outer, text="🚭", font=("Segoe UI", 56),
                 bg=COLORS["bg"], fg=COLORS["green"]).pack()

        tk.Label(outer, text="SIN HUMO",
                 font=("Segoe UI", 30, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack()

        tk.Label(outer, text="Tu asistente de ahorro por dejar de fumar",
                 font=("Segoe UI", 12),
                 bg=COLORS["bg"], fg=COLORS["subtext"]).pack(pady=(2, 25))

        card = tk.Frame(outer, bg=COLORS["card"], padx=35, pady=30)
        card.pack(fill="x")

        # Quit date
        self._label(card, "¿Cuándo dejaste de fumar?  (DD/MM/AAAA)").pack(anchor="w")
        date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        date_entry = self._entry(card, textvariable=date_var)
        date_entry.pack(anchor="w", pady=(5, 20), ipady=7, ipadx=6)

        # Daily cost
        self._label(card, "¿Cuánto gastabas en tabaco al día? (€)").pack(anchor="w")
        tk.Label(card, text="Ej: si fumabas un paquete de 5,00 € al día escribe 5",
                 font=("Segoe UI", 9), bg=COLORS["card"], fg=COLORS["subtext"]).pack(anchor="w")
        cost_var = tk.StringVar(value="5.00")
        cost_entry = self._entry(card, textvariable=cost_var)
        cost_entry.pack(anchor="w", pady=(5, 20), ipady=7, ipadx=6)

        # Cigarettes per day
        self._label(card, "¿Cuántos cigarrillos fumabas al día?").pack(anchor="w")
        cigs_var = tk.StringVar(value="20")
        cigs_entry = self._entry(card, textvariable=cigs_var)
        cigs_entry.pack(anchor="w", pady=(5, 20), ipady=7, ipadx=6)

        err_lbl = tk.Label(card, text="", font=("Segoe UI", 9),
                           bg=COLORS["card"], fg=COLORS["red"])
        err_lbl.pack(anchor="w")

        def on_save():
            err_lbl.config(text="")
            try:
                quit_dt = datetime.strptime(date_var.get().strip(), "%d/%m/%Y").date()
            except ValueError:
                err_lbl.config(text="⚠  Fecha inválida. Usa el formato DD/MM/AAAA")
                return
            try:
                daily_cost = float(cost_var.get().strip().replace(",", "."))
                if daily_cost <= 0:
                    raise ValueError
            except ValueError:
                err_lbl.config(text="⚠  Coste inválido. Escribe un número positivo")
                return
            try:
                cigs = int(cigs_var.get().strip())
                if cigs <= 0:
                    raise ValueError
            except ValueError:
                err_lbl.config(text="⚠  Número de cigarrillos inválido")
                return
            if quit_dt > date.today():
                err_lbl.config(text="⚠  La fecha no puede ser en el futuro")
                return

            self.config = {
                "quit_date":    quit_dt.isoformat(),
                "daily_cost":   daily_cost,
                "cigs_per_day": cigs,
            }
            self._save_config()
            self._show_main()

        tk.Button(card, text="¡Empezar a ahorrar!  💚",
                  font=("Segoe UI", 12, "bold"),
                  bg=COLORS["green"], fg="white",
                  relief="flat", padx=22, pady=11,
                  cursor="hand2", bd=0,
                  activebackground=COLORS["light_green"],
                  command=on_save).pack(pady=(10, 0))

    # ── Main screen ──────────────────────────────────────────────────────────

    def _show_main(self):
        self._clear()

        canvas = tk.Canvas(self.root, bg=COLORS["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(self.root, orient="vertical",
                            command=canvas.yview, style="Dark.TScrollbar")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas, bg=COLORS["bg"])
        win_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        def _on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win_id, width=canvas.winfo_width())

        frame.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=canvas.winfo_width()))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), "units"))

        self._build_main_content(frame)
        self.root.after(300000, self._show_main)   # auto-refresh every 5 min

    def _build_main_content(self, parent):
        s = self._calc()
        best, nxt = self._get_items_for(s["total"])
        quote = MOTIVATIONAL_QUOTES[self._quote_index % len(MOTIVATIONAL_QUOTES)]
        quote = quote.replace("{days}", str(s["days"]))
        self._quote_index += 1

        pad = {"padx": 18, "pady": 6}

        # ── Header ─────────────────────────────────────────────────────
        hdr = tk.Frame(parent, bg=COLORS["accent"], pady=18)
        hdr.pack(fill="x")
        hdr_inner = tk.Frame(hdr, bg=COLORS["accent"])
        hdr_inner.pack(fill="x", padx=25)

        tk.Label(hdr_inner, text="🚭  SIN HUMO",
                 font=("Segoe UI", 20, "bold"),
                 bg=COLORS["accent"], fg=COLORS["green"]).pack(side="left")

        total_lbl = tk.Label(hdr_inner,
                             text=f"💰  {s['total']:.2f} € ahorrados",
                             font=("Segoe UI", 17, "bold"),
                             bg=COLORS["accent"], fg=COLORS["yellow"])
        total_lbl.pack(side="right")

        # ── Days banner ────────────────────────────────────────────────
        banner = tk.Frame(parent, bg=COLORS["card2"], pady=16, padx=25)
        banner.pack(fill="x", **pad)

        tk.Label(banner,
                 text=f"🗓️   {s['days']} días sin fumar",
                 font=("Segoe UI", 18, "bold"),
                 bg=COLORS["card2"], fg=COLORS["green"]).pack(anchor="w")
        tk.Label(banner, text=quote,
                 font=("Segoe UI", 10, "italic"),
                 bg=COLORS["card2"], fg=COLORS["subtext"],
                 wraplength=700, justify="left").pack(anchor="w", pady=(4, 0))

        # ── Savings grid ───────────────────────────────────────────────
        sec_lbl = tk.Label(parent, text="  📊  TUS AHORROS",
                           font=("Segoe UI", 10, "bold"),
                           bg=COLORS["bg"], fg=COLORS["subtext"])
        sec_lbl.pack(anchor="w", padx=18, pady=(10, 2))

        grid = tk.Frame(parent, bg=COLORS["bg"])
        grid.pack(fill="x", **pad)

        savings_cards = [
            ("📅 Esta semana",  f"{s['this_week']:.2f} €",  "Ahorrado desde el lunes"),
            ("📆 Por semana",   f"{s['weekly']:.2f} €",     "Ahorro semanal habitual"),
            ("🗓️ Por quincena", f"{s['biweekly']:.2f} €",   "Cada 15 días"),
            ("📅 Este mes",     f"{s['this_month']:.2f} €", "Ahorrado este mes"),
            ("🗓️ Por mes",      f"{s['monthly']:.2f} €",    "Ahorro mensual habitual"),
            ("📈 Por año",      f"{s['yearly']:.2f} €",     "Proyección anual"),
        ]

        for i, (title, amount, sub) in enumerate(savings_cards):
            col = i % 3
            if col == 0:
                row_f = tk.Frame(grid, bg=COLORS["bg"])
                row_f.pack(fill="x", pady=3)
            c = tk.Frame(row_f, bg=COLORS["card"], pady=13, padx=16)
            c.pack(side="left", fill="x", expand=True, padx=3)
            tk.Label(c, text=title,  font=("Segoe UI", 9),
                     bg=COLORS["card"], fg=COLORS["subtext"]).pack(anchor="w")
            tk.Label(c, text=amount, font=("Segoe UI", 16, "bold"),
                     bg=COLORS["card"], fg=COLORS["green"]).pack(anchor="w")
            tk.Label(c, text=sub,    font=("Segoe UI", 8),
                     bg=COLORS["card"], fg=COLORS["subtext"]).pack(anchor="w")

        # ── Best purchase you can afford ───────────────────────────────
        tk.Label(parent, text="  🎉  ¡CON TU AHORRO ACTUAL PUEDES COMPRAR!",
                 font=("Segoe UI", 10, "bold"),
                 bg=COLORS["bg"], fg=COLORS["yellow"]).pack(anchor="w", padx=18, pady=(14, 2))

        if best:
            bc = tk.Frame(parent, bg="#0d3320", pady=14, padx=22)
            bc.pack(fill="x", **pad)
            tk.Label(bc, text=best[1],
                     font=("Segoe UI", 15, "bold"),
                     bg="#0d3320", fg=COLORS["light_green"]).pack(anchor="w")
            tk.Label(bc, text=f"Precio aprox: {best[0]} €   ·   {best[2]}",
                     font=("Segoe UI", 9),
                     bg="#0d3320", fg=COLORS["subtext"]).pack(anchor="w", pady=(3, 0))
        else:
            no_c = tk.Frame(parent, bg=COLORS["card"], pady=12, padx=22)
            no_c.pack(fill="x", **pad)
            tk.Label(no_c,
                     text="Sigue sin fumar y pronto podrás darte un capricho 💪",
                     font=("Segoe UI", 11),
                     bg=COLORS["card"], fg=COLORS["subtext"]).pack(anchor="w")

        # ── Next goal ──────────────────────────────────────────────────
        if nxt:
            needed     = nxt[0] - s["total"]
            days_left  = math.ceil(needed / s["daily"]) if s["daily"] > 0 else 0
            progress   = min(s["total"] / nxt[0], 1.0)

            tk.Label(parent, text="  🎯  TU PRÓXIMO OBJETIVO",
                     font=("Segoe UI", 10, "bold"),
                     bg=COLORS["bg"], fg=COLORS["orange"]).pack(anchor="w", padx=18, pady=(14, 2))

            nc = tk.Frame(parent, bg="#1f0e00", pady=14, padx=22)
            nc.pack(fill="x", **pad)

            tk.Label(nc, text=nxt[1],
                     font=("Segoe UI", 14, "bold"),
                     bg="#1f0e00", fg=COLORS["yellow"]).pack(anchor="w")
            tk.Label(nc,
                     text=f"Te faltan {needed:.2f} €  ·  En {days_left} días más sin fumar lo consigues!",
                     font=("Segoe UI", 9),
                     bg="#1f0e00", fg=COLORS["subtext"]).pack(anchor="w", pady=(3, 6))

            # Progress bar via Canvas
            bar_frame = tk.Frame(nc, bg="#1f0e00")
            bar_frame.pack(fill="x")
            bar_canvas = tk.Canvas(bar_frame, height=14, bg="#3a1e00",
                                   highlightthickness=0, relief="flat")
            bar_canvas.pack(fill="x")

            def _draw_bar(event=None):
                w = bar_canvas.winfo_width()
                bar_canvas.delete("all")
                bar_canvas.create_rectangle(0, 0, int(w * progress), 14,
                                            fill=COLORS["orange"], outline="")
                pct = f"{int(progress * 100)}%"
                bar_canvas.create_text(w // 2, 7, text=pct,
                                       fill="white", font=("Segoe UI", 8, "bold"))

            bar_canvas.bind("<Configure>", _draw_bar)
            bar_canvas.after(50, _draw_bar)

            tk.Label(nc,
                     text=f"  {nxt[2]}",
                     font=("Segoe UI", 9, "italic"),
                     bg="#1f0e00", fg=COLORS["subtext"]).pack(anchor="w", pady=(5, 0))

        # ── Health stats ───────────────────────────────────────────────
        tk.Label(parent, text="  💪  TU CUERPO TE LO AGRADECE",
                 font=("Segoe UI", 10, "bold"),
                 bg=COLORS["bg"], fg=COLORS["light_green"]).pack(anchor="w", padx=18, pady=(14, 2))

        health_row = tk.Frame(parent, bg=COLORS["bg"])
        health_row.pack(fill="x", **pad)

        health_items = [
            ("🚬", f"{s['cigs_avoided']:,}", "Cigarrillos no fumados"),
            ("⏱️", f"{s['minutes_won']:,}", "Minutos de vida ganados"),
            ("❤️", "Mejorando", "Tu corazón día a día"),
            ("🫁", "Limpiando", "Tus pulmones se recuperan"),
        ]
        for icon, val, lbl in health_items:
            hc = tk.Frame(health_row, bg=COLORS["card"], pady=12, padx=12)
            hc.pack(side="left", fill="x", expand=True, padx=3)
            tk.Label(hc, text=icon, font=("Segoe UI", 18),
                     bg=COLORS["card"]).pack()
            tk.Label(hc, text=val,  font=("Segoe UI", 13, "bold"),
                     bg=COLORS["card"], fg=COLORS["light_green"]).pack()
            tk.Label(hc, text=lbl,  font=("Segoe UI", 8),
                     bg=COLORS["card"], fg=COLORS["subtext"],
                     wraplength=120, justify="center").pack()

        # ── Wishlist ───────────────────────────────────────────────────
        tk.Label(parent, text="  🛒  LISTA DE CAPRICHOS",
                 font=("Segoe UI", 10, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", padx=18, pady=(14, 2))
        tk.Label(parent,
                 text="  Cuanto más ahorres, más caprichos podrás permitirte:",
                 font=("Segoe UI", 9),
                 bg=COLORS["bg"], fg=COLORS["subtext"]).pack(anchor="w", padx=18)

        wish = tk.Frame(parent, bg=COLORS["bg"])
        wish.pack(fill="x", padx=18, pady=(6, 0))

        # Show items up to 2× current savings (with at least the first 6)
        threshold = max(s["total"] * 2, MOTIVATIONAL_ITEMS[5][0])
        items_to_show = [x for x in MOTIVATIONAL_ITEMS if x[0] <= threshold][:16]

        for price, item, _ in items_to_show:
            row = tk.Frame(wish, bg=COLORS["card"], pady=8, padx=16)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=item, font=("Segoe UI", 10, "bold"),
                     bg=COLORS["card"], fg=COLORS["text"]).pack(side="left")
            tk.Label(row, text=f"  {price} €  ", font=("Segoe UI", 9),
                     bg=COLORS["card"], fg=COLORS["subtext"]).pack(side="left")

            if price <= s["total"]:
                status_txt = "✅  ¡PUEDES COMPRARLO!"
                status_col = COLORS["green"]
            else:
                dl = math.ceil((price - s["total"]) / s["daily"]) if s["daily"] > 0 else 0
                status_txt = f"⏳  En {dl} días"
                status_col = COLORS["orange"]

            tk.Label(row, text=status_txt, font=("Segoe UI", 9, "bold"),
                     bg=COLORS["card"], fg=status_col).pack(side="right")

        # ── Footer buttons ─────────────────────────────────────────────
        btns = tk.Frame(parent, bg=COLORS["bg"])
        btns.pack(fill="x", padx=18, pady=(20, 30))

        tk.Button(btns, text="⚙️  Cambiar configuración",
                  font=("Segoe UI", 10),
                  bg=COLORS["accent"], fg=COLORS["text"],
                  relief="flat", padx=16, pady=9, cursor="hand2", bd=0,
                  activebackground=COLORS["card"],
                  command=self._show_setup).pack(side="left", padx=(0, 8))

        tk.Button(btns, text="🔄  Actualizar ahora",
                  font=("Segoe UI", 10),
                  bg=COLORS["green"], fg="white",
                  relief="flat", padx=16, pady=9, cursor="hand2", bd=0,
                  activebackground=COLORS["light_green"],
                  command=self._show_main).pack(side="left")

        tk.Label(btns,
                 text=f"Actualizado: {datetime.now().strftime('%H:%M  ·  %d/%m/%Y')}",
                 font=("Segoe UI", 8),
                 bg=COLORS["bg"], fg=COLORS["subtext"]).pack(side="right")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _label(self, parent, text):
        return tk.Label(parent, text=text,
                        font=("Segoe UI", 11, "bold"),
                        bg=COLORS["card"], fg=COLORS["text"])

    def _entry(self, parent, **kw):
        e = tk.Entry(parent, font=("Segoe UI", 13), width=24,
                     bg=COLORS["accent"], fg=COLORS["text"],
                     insertbackground=COLORS["text"],
                     relief="flat",
                     highlightthickness=1,
                     highlightbackground=COLORS["border"],
                     highlightcolor=COLORS["green"],
                     **kw)
        return e


def main():
    root = tk.Tk()
    app = SinHumoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
