# modules/ui/power_grid_sabotage.py
import customtkinter as ctk
import random
import threading
import time

class PowerGridSabotagePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.is_sabotaging = False
        self.sabotage_progress = 0
        self.active_blackouts = {}
        
        # Définition des zones et quartiers
        self.ZONES = {
            "Los Santos": {
                "color": "#ff6b35",
                "districts": [
                    {"name": "Downtown LS", "id": "downtown_ls", "population": 15000},
                    {"name": "Pillbox Hill", "id": "pillbox", "population": 8500},
                    {"name": "Integrity Way", "id": "integrity", "population": 6200},
                    {"name": "Legion Square", "id": "legion", "population": 9800},
                    {"name": "Rockford Hills", "id": "rockford", "population": 12000},
                    {"name": "Vinewood", "id": "vinewood", "population": 14500},
                    {"name": "Del Perro", "id": "delperro", "population": 11000},
                    {"name": "Sandy Shores", "id": "sandy", "population": 3200},
                    {"name": "Paleto Bay", "id": "paleto", "population": 2100},
                    {"name": "Blaine County", "id": "blaine_main", "population": 5000},
                ]
            },
            "Blaine County": {
                "color": "#45a29e",
                "districts": [
                    {"name": "Fort Zancudo", "id": "fort_z", "population": 800},
                    {"name": "Grapeseed", "id": "grapeseed", "population": 4200},
                    {"name": "Alamo Sea", "id": "alamo", "population": 1500},
                    {"name": "Chiliad Mountain", "id": "chiliad", "population": 900},
                    {"name": "Whinyard Creek", "id": "whinyard", "population": 2300},
                    {"name": "Harmony", "id": "harmony", "population": 1800},
                    {"name": "Sandy Diesel", "id": "sandy_diesel", "population": 3100},
                ]
            }
        }
        
        # --- TITRE ---
        self.title_label = ctk.CTkLabel(
            self,
            text="⚡ CENTRAL ÉLECTRIQUE - Contrôle du Réseau",
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#ff6b35"
        )
        self.title_label.pack(pady=(15, 10))
        
        # --- INFOS GÉNÉRALES ---
        self.info_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", border_width=2, border_color="#ffb703")
        self.info_frame.pack(pady=10, padx=15, fill="x")
        
        self.status_label = ctk.CTkLabel(
            self.info_frame,
            text="🟢 Réseau stable",
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color="#00ff00"
        )
        self.status_label.pack(side="left", padx=15, pady=10)
        
        self.blackout_count_label = ctk.CTkLabel(
            self.info_frame,
            text="Secteurs affectés: 0",
            font=ctk.CTkFont(family="Courier", size=12),
            text_color="#ffb703"
        )
        self.blackout_count_label.pack(side="right", padx=15, pady=10)
        
        # --- SCROLL FRAME PRINCIPAL ---
        self.main_scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#0d0d0d")
        self.main_scroll_frame.pack(pady=10, padx=15, fill="both", expand=True)
        
        # Créer les panneaux pour chaque zone
        self.zone_panels = {}
        for zone_name, zone_data in self.ZONES.items():
            self.create_zone_panel(zone_name, zone_data)
        
        # --- TERMINAL DE LOG ---
        self.terminal_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", border_width=2, border_color="#00ff00")
        self.terminal_frame.pack(pady=10, padx=15, fill="both", expand=False, ipady=5)
        
        self.terminal_label = ctk.CTkLabel(
            self.terminal_frame,
            text="📡 TERMINAL DE MONITORING",
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            text_color="#00ff00"
        )
        self.terminal_label.pack(anchor="w", padx=10, pady=5)
        
        self.terminal_box = ctk.CTkTextbox(
            self.terminal_frame,
            fg_color="#0d0d0d",
            text_color="#00ff00",
            font=ctk.CTkFont(family="Courier", size=10),
            height=100
        )
        self.terminal_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.terminal_box.configure(state="disabled")
        
        self.add_log("[SYSTÈME] Central électrique initialisée")
        self.add_log("[SYSTÈME] Tous les secteurs sont normaux")
    
    def create_zone_panel(self, zone_name, zone_data):
        """Crée un panneau pour une zone avec ses quartiers."""
        
        # Panneau de zone
        zone_panel = ctk.CTkFrame(self.main_scroll_frame, fg_color="#1a1a1a", border_width=2, border_color=zone_data["color"])
        zone_panel.pack(pady=10, padx=0, fill="x")
        
        # Titre de la zone
        zone_title = ctk.CTkLabel(
            zone_panel,
            text=f"📍 {zone_name}",
            font=ctk.CTkFont(family="Courier", size=16, weight="bold"),
            text_color=zone_data["color"]
        )
        zone_title.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Grille de toggles pour les quartiers
        districts = zone_data["districts"]
        self.zone_panels[zone_name] = {}
        
        # Créer une grille scrollable pour les quartiers
        districts_scroll = ctk.CTkScrollableFrame(zone_panel, fg_color="#0d0d0d", height=200)
        districts_scroll.pack(padx=10, pady=10, fill="both", expand=False)
        
        for i, district in enumerate(districts):
            district_frame = ctk.CTkFrame(districts_scroll, fg_color="#1a1a1a", border_width=1, border_color="#333333")
            district_frame.pack(fill="x", padx=5, pady=5)
            
            # Nom du quartier + infos
            info_frame = ctk.CTkFrame(district_frame, fg_color="#1a1a1a")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
            
            district_label = ctk.CTkLabel(
                info_frame,
                text=f"🏙️  {district['name']}",
                font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
                text_color="#ffffff"
            )
            district_label.pack(anchor="w")
            
            population_label = ctk.CTkLabel(
                info_frame,
                text=f"👥 Population: {district['population']:,} habitants",
                font=ctk.CTkFont(family="Courier", size=10),
                text_color="#ffb703"
            )
            population_label.pack(anchor="w")
            
            # Toggle avec callback
            toggle_var = ctk.BooleanVar(value=False)
            toggle = ctk.CTkSwitch(
                district_frame,
                text="",
                variable=toggle_var,
                onvalue=True,
                offvalue=False,
                fg_color="#45a29e",
                progress_color="#ff6b35",
                font=ctk.CTkFont(family="Courier", size=12),
                command=self.update_network_status
            )
            toggle.pack(side="right", padx=10, pady=8)
            
            # Stocker la variable et les infos
            self.zone_panels[zone_name][district['id']] = {
                "var": toggle_var,
                "name": district['name'],
                "population": district['population'],
                "label": population_label,
                "status": "normal"
            }
    
    def add_log(self, message):
        """Ajoute un message au terminal."""
        self.terminal_box.configure(state="normal")
        self.terminal_box.insert("end", message + "\n")
        self.terminal_box.see("end")
        self.terminal_box.configure(state="disabled")
    
    def count_selected_districts(self):
        """Compte le nombre de quartiers sélectionnés."""
        count = 0
        for zone_name, districts in self.zone_panels.items():
            for district_id, data in districts.items():
                if data["var"].get():
                    count += 1
        return count
    
    def update_network_status(self):
        """Met à jour le statut du réseau en temps réel."""
        selected_count = self.count_selected_districts()
        
        # Déterminer le statut en fonction du nombre de quartiers sélectionnés
        if selected_count == 0:
            status_text = "🟢 Réseau stable"
            status_color = "#00ff00"
        elif selected_count < 5:
            status_text = "🟠 Réseau perturbé"
            status_color = "#ffaa00"
        elif selected_count < 10:
            status_text = "🟡 Réseau instable"
            status_color = "#ffff00"
        elif selected_count < 15:
            status_text = "🔴 Réseau impacté"
            status_color = "#ff6b35"
        else:
            status_text = "🔴 RÉSEAU PIRATÉ"
            status_color = "#ff0000"
        
        self.status_label.configure(text=status_text, text_color=status_color)
        self.blackout_count_label.configure(text=f"Secteurs affectés: {selected_count}")
        
        # Log la modification
        if selected_count > 0:
            self.add_log(f"[⚠️  ] Configuration modifiée - {selected_count} secteur(s) ciblé(s)")