"""
Design system and styling for MedLink
Professional medical theme with modern look
"""
import customtkinter as ctk

# Color palette
COLORS = {
    # Primary colors
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'secondary': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',

    # Backgrounds
    'bg_dark': '#0f172a',
    'bg_medium': '#1e293b',
    'bg_light': '#334155',
    'bg_hover': '#475569',

    # Text
    'text_primary': '#f8fafc',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',

    # Status colors
    'success': '#10b981',
    'error': '#ef4444',
    'info': '#06b6d4',

    # Accents
    'accent_purple': '#8b5cf6',
    'accent_cyan': '#06b6d4',
}

# Fonts
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 18, 'bold'),
    'subheading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 12),
    'body_bold': ('Segoe UI', 12, 'bold'),
    'small': ('Segoe UI', 10),
    'code': ('Consolas', 11),
}

# Spacing
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
}

# Border radius
RADIUS = {
    'sm': 4,
    'md': 8,
    'lg': 12,
    'full': 16,
}


def setup_theme():
    """Configure CustomTkinter theme"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


def create_card_frame(parent, **kwargs):
    """Create a styled card frame"""
    return ctk.CTkFrame(
        parent,
        fg_color=COLORS['bg_light'],
        corner_radius=RADIUS['md'],
        **kwargs
    )


def create_button(parent, text, command=None, style='primary', **kwargs):
    """Create a styled button"""
    colors = {
        'primary': (COLORS['primary'], COLORS['primary_hover']),
        'secondary': (COLORS['secondary'], '#059669'),
        'danger': (COLORS['danger'], '#dc2626'),
    }

    fg_color, hover_color = colors.get(style, colors['primary'])

    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=fg_color,
        hover_color=hover_color,
        font=FONTS['body_bold'],
        corner_radius=RADIUS['md'],
        **kwargs
    )


def create_entry(parent, placeholder="", **kwargs):
    """Create a styled entry field"""
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        font=FONTS['body'],
        corner_radius=RADIUS['md'],
        border_width=2,
        **kwargs
    )


def create_label(parent, text, style='body', **kwargs):
    """Create a styled label"""
    return ctk.CTkLabel(
        parent,
        text=text,
        font=FONTS.get(style, FONTS['body']),
        text_color=COLORS['text_primary'],
        **kwargs
    )
