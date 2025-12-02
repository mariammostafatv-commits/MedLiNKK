"""
Enhanced imaging results manager - Display and manage imaging results
Location: gui/components/enhanced_imaging_results_manager.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.imaging_manager import imaging_manager
from PIL import Image
import os


class EnhancedImagingResultsManager(ctk.CTkFrame):
    """Enhanced imaging results display with image viewing"""
    
    def __init__(self, parent, patient_data, is_doctor=False):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.is_doctor = is_doctor
        self.all_results = []
        self.filtered_results = []
        
        self.create_ui()
        self.load_results()
    
    def create_ui(self):
        """Create imaging results UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="🏥 Medical Imaging",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(side='left')
        
        # Add button (doctor only)
        if self.is_doctor:
            add_btn = ctk.CTkButton(
                header,
                text="+ Add Imaging",
                command=self.add_imaging_result,
                font=FONTS['body_bold'],
                height=40,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            add_btn.pack(side='right')
        
        # Filter Bar
        filter_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=RADIUS['lg'])
        filter_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        filter_content = ctk.CTkFrame(filter_frame, fg_color='transparent')
        filter_content.pack(fill='x', padx=20, pady=15)
        
        # Search
        search_frame = ctk.CTkFrame(filter_content, fg_color='transparent')
        search_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Search:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        search_label.pack(side='left', padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search imaging type or body part...",
            font=FONTS['body'],
            height=40
        )
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind('<KeyRelease>', lambda e: self.apply_filters())
        
        # Filter by modality
        modality_frame = ctk.CTkFrame(filter_content, fg_color='transparent')
        modality_frame.pack(side='left')
        
        modality_label = ctk.CTkLabel(
            modality_frame,
            text="Modality:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        modality_label.pack(side='left', padx=(0, 10))
        
        self.modality_filter = ctk.CTkOptionMenu(
            modality_frame,
            values=["All", "X-Ray", "CT Scan", "MRI", "Ultrasound", "PET Scan", "Mammogram", "Other"],
            command=lambda x: self.apply_filters(),
            font=FONTS['body'],
            height=40,
            width=150
        )
        self.modality_filter.pack(side='left')
        
        # Results container
        self.results_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.results_scroll.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def load_results(self):
        """Load all imaging results"""
        self.all_results = imaging_manager.get_patient_imaging_results(
            self.patient_data.get('national_id')
        )
        self.apply_filters()
    
    def apply_filters(self):
        """Apply search and modality filters"""
        search_text = self.search_entry.get().lower()
        modality = self.modality_filter.get()
        
        # Filter results
        self.filtered_results = []
        for result in self.all_results:
            # Modality filter
            if modality != "All" and result.get('modality', 'Other') != modality:
                continue
            
            # Search filter
            if search_text:
                imaging_type = result.get('imaging_type', '').lower()
                body_part = result.get('body_part', '').lower()
                if search_text not in imaging_type and search_text not in body_part:
                    continue
            
            self.filtered_results.append(result)
        
        self.display_results()
    
    def display_results(self):
        """Display filtered results"""
        # Clear existing
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        if not self.filtered_results:
            no_data = ctk.CTkLabel(
                self.results_scroll,
                text="No imaging results found" if not self.all_results else "No results match your filters",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=50)
            return
        
        # Group by date
        results_by_date = {}
        for result in self.filtered_results:
            date = result.get('date', 'Unknown')
            if date not in results_by_date:
                results_by_date[date] = []
            results_by_date[date].append(result)
        
        # Display by date (newest first)
        sorted_dates = sorted(results_by_date.keys(), reverse=True)
        
        for date in sorted_dates:
            # Date header
            date_header = ctk.CTkFrame(
                self.results_scroll,
                fg_color='transparent'
            )
            date_header.pack(fill='x', pady=(10, 5))
            
            date_label = ctk.CTkLabel(
                date_header,
                text=f"📅 {date}",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            date_label.pack(anchor='w')
            
            # Results for this date
            for result in results_by_date[date]:
                self.create_result_card(result)
    
    def create_result_card(self, result):
        """Create card for single imaging result"""
        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(fill='x', pady=5)
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', padx=20, pady=15)
        
        # Header row
        header_row = ctk.CTkFrame(content, fg_color='transparent')
        header_row.pack(fill='x', pady=(0, 10))
        
        # Imaging type and modality badge
        left_frame = ctk.CTkFrame(header_row, fg_color='transparent')
        left_frame.pack(side='left', fill='x', expand=True)
        
        imaging_type = ctk.CTkLabel(
            left_frame,
            text=f"🏥 {result.get('imaging_type', 'Unknown')} - {result.get('body_part', 'N/A')}",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        imaging_type.pack(side='left')
        
        # Modality badge
        modality = result.get('modality', 'Other')
        badge_color = self.get_modality_color(modality)
        
        modality_badge = ctk.CTkFrame(
            left_frame,
            fg_color=badge_color,
            corner_radius=RADIUS['sm'],
            height=24
        )
        modality_badge.pack(side='left', padx=(10, 0))
        
        modality_label = ctk.CTkLabel(
            modality_badge,
            text=modality,
            font=FONTS['small_bold'],
            text_color='white'
        )
        modality_label.pack(padx=10, pady=3)
        
        # Status badge
        status = result.get('status', 'Completed')
        status_color = COLORS['success'] if status == 'Completed' else COLORS['warning']
        
        status_badge = ctk.CTkFrame(
            header_row,
            fg_color=status_color,
            corner_radius=RADIUS['sm'],
            height=24
        )
        status_badge.pack(side='right')
        
        status_label = ctk.CTkLabel(
            status_badge,
            text=status,
            font=FONTS['small_bold'],
            text_color='white'
        )
        status_label.pack(padx=10, pady=3)
        
        # Details
        details_frame = ctk.CTkFrame(content, fg_color='transparent')
        details_frame.pack(fill='x', pady=(0, 10))
        
        # Facility and Radiologist
        facility_info = f"🏥 {result.get('facility', 'N/A')} | 👨‍⚕️ {result.get('radiologist', 'N/A')}"
        facility_label = ctk.CTkLabel(
            details_frame,
            text=facility_info,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        facility_label.pack(anchor='w')
        
        # Findings (preview)
        if result.get('findings'):
            findings_preview = result['findings'][:150]
            if len(result['findings']) > 150:
                findings_preview += "..."
            
            findings_label = ctk.CTkLabel(
                content,
                text=f"📋 Findings: {findings_preview}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=600,
                justify='left'
            )
            findings_label.pack(anchor='w', pady=(0, 10))
        
        # Impression (preview)
        if result.get('impression'):
            impression_preview = result['impression'][:100]
            if len(result['impression']) > 100:
                impression_preview += "..."
            
            impression_label = ctk.CTkLabel(
                content,
                text=f"💡 Impression: {impression_preview}",
                font=FONTS['small_bold'],
                text_color=COLORS['text_primary'],
                wraplength=600,
                justify='left'
            )
            impression_label.pack(anchor='w', pady=(0, 10))
        
        # Actions
        actions_frame = ctk.CTkFrame(content, fg_color='transparent')
        actions_frame.pack(fill='x')
        
        # View report button
        view_btn = ctk.CTkButton(
            actions_frame,
            text="📄 View Report",
            command=lambda r=result: self.view_full_report(r),
            font=FONTS['small_bold'],
            height=35,
            fg_color=COLORS['info'],
            hover_color='#0284c7'
        )
        view_btn.pack(side='left', padx=(0, 10))
        
        # View images button (if images available)
        if result.get('image_paths'):
            view_images_btn = ctk.CTkButton(
                actions_frame,
                text="🖼️ View Images",
                command=lambda r=result: self.view_images(r),
                font=FONTS['small_bold'],
                height=35,
                fg_color=COLORS['primary'],
                hover_color='#2563eb'
            )
            view_images_btn.pack(side='left', padx=(0, 10))
        
        # Download PDF (if available)
        if result.get('report_path'):
            download_btn = ctk.CTkButton(
                actions_frame,
                text="💾 Download",
                command=lambda r=result: self.download_report(r),
                font=FONTS['small_bold'],
                height=35,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            download_btn.pack(side='left')
    
    def get_modality_color(self, modality):
        """Get color for modality badge"""
        colors = {
            'X-Ray': '#3B82F6',
            'CT Scan': '#8B5CF6',
            'MRI': '#EC4899',
            'Ultrasound': '#10B981',
            'PET Scan': '#F59E0B',
            'Mammogram': '#EF4444',
            'Other': '#6B7280'
        }
        return colors.get(modality, '#6B7280')
    
    def view_full_report(self, result):
        """View full imaging report"""
        # Create detailed view dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Imaging Report: {result.get('imaging_type', 'N/A')}")
        dialog.geometry("700x800")
        
        # Center on parent
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        # Header
        header = ctk.CTkFrame(dialog, fg_color=COLORS['bg_medium'])
        header.pack(fill='x', padx=30, pady=(30, 0))
        
        title = ctk.CTkLabel(
            header,
            text=f"{result.get('imaging_type', 'Imaging Report')} - {result.get('body_part', 'N/A')}",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(padx=20, pady=15)
        
        # Content
        scroll = ctk.CTkScrollableFrame(dialog, fg_color='transparent')
        scroll.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Date and Modality
        date_label = ctk.CTkLabel(
            scroll,
            text=f"📅 Date: {result.get('date', 'N/A')} | 🏥 Modality: {result.get('modality', 'N/A')}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        date_label.pack(anchor='w', pady=(0, 10))
        
        # Facility and Radiologist
        facility_label = ctk.CTkLabel(
            scroll,
            text=f"🏥 Facility: {result.get('facility', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        facility_label.pack(anchor='w', pady=3)
        
        radiologist_label = ctk.CTkLabel(
            scroll,
            text=f"👨‍⚕️ Radiologist: {result.get('radiologist', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        radiologist_label.pack(anchor='w', pady=3)
        
        # Indication
        if result.get('indication'):
            indication_title = ctk.CTkLabel(
                scroll,
                text="Clinical Indication:",
                font=FONTS['subheading'],
                text_color=COLORS['text_primary']
            )
            indication_title.pack(anchor='w', pady=(20, 10))
            
            indication_text = ctk.CTkLabel(
                scroll,
                text=result['indication'],
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                wraplength=600,
                justify='left'
            )
            indication_text.pack(anchor='w')
        
        # Findings
        if result.get('findings'):
            findings_title = ctk.CTkLabel(
                scroll,
                text="Findings:",
                font=FONTS['subheading'],
                text_color=COLORS['text_primary']
            )
            findings_title.pack(anchor='w', pady=(20, 10))
            
            findings_box = ctk.CTkFrame(
                scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            findings_box.pack(fill='x')
            
            findings_text = ctk.CTkLabel(
                findings_box,
                text=result['findings'],
                font=FONTS['body'],
                text_color=COLORS['text_primary'],
                wraplength=600,
                justify='left'
            )
            findings_text.pack(padx=15, pady=15)
        
        # Impression
        if result.get('impression'):
            impression_title = ctk.CTkLabel(
                scroll,
                text="Impression:",
                font=FONTS['subheading'],
                text_color=COLORS['text_primary']
            )
            impression_title.pack(anchor='w', pady=(20, 10))
            
            impression_box = ctk.CTkFrame(
                scroll,
                fg_color=COLORS['info'],
                corner_radius=RADIUS['md']
            )
            impression_box.pack(fill='x')
            
            impression_text = ctk.CTkLabel(
                impression_box,
                text=result['impression'],
                font=FONTS['body_bold'],
                text_color='white',
                wraplength=600,
                justify='left'
            )
            impression_text.pack(padx=15, pady=15)
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['danger'],
            hover_color='#dc2626'
        )
        close_btn.pack(fill='x', padx=30, pady=(0, 30))
    
    def view_images(self, result):
        """View imaging images"""
        image_paths = result.get('image_paths', [])
        
        if not image_paths:
            messagebox.showinfo("No Images", "No images available for this study")
            return
        
        # Create image viewer dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Images: {result.get('imaging_type', 'N/A')}")
        dialog.geometry("900x700")
        
        # Center on parent
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        # Content
        content = ctk.CTkFrame(dialog, fg_color=COLORS['bg_dark'])
        content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header_label = ctk.CTkLabel(
            content,
            text=f"📸 {len(image_paths)} Image(s) Available",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        header_label.pack(pady=(0, 20))
        
        # Image grid
        grid_frame = ctk.CTkScrollableFrame(content, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True)
        
        # Display image thumbnails
        for i, img_path in enumerate(image_paths):
            img_card = ctk.CTkFrame(
                grid_frame,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            img_card.pack(fill='x', pady=5)
            
            img_label = ctk.CTkLabel(
                img_card,
                text=f"📄 Image {i+1}: {os.path.basename(img_path)}",
                font=FONTS['body'],
                text_color=COLORS['text_primary']
            )
            img_label.pack(padx=15, pady=15)
        
        # Close button
        close_btn = ctk.CTkButton(
            content,
            text="Close",
            command=dialog.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['danger'],
            hover_color='#dc2626'
        )
        close_btn.pack(fill='x', pady=(20, 0))
    
    def download_report(self, result):
        """Download imaging report PDF"""
        report_path = result.get('report_path')
        if report_path and os.path.exists(report_path):
            messagebox.showinfo("Download", f"Report available at: {report_path}")
        else:
            messagebox.showwarning("Not Available", "Report file not found")
    
    def add_imaging_result(self):
        """Open dialog to add new imaging result (doctor only)"""
        messagebox.showinfo("Add Imaging", "Imaging entry dialog would open here")
        # This would open a comprehensive imaging entry dialog