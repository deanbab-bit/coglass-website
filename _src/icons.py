"""Thin line icons (30×30, stroke = currentColor via .ico / .tile svg). No emoji."""

def _i(paths):
    return f'<svg class="ico" viewBox="0 0 30 30" aria-hidden="true" focusable="false">{paths}</svg>'

ICON = {
    'shaped': _i('<path d="M5 25V12a10 10 0 0 1 20 0v13z"/><circle cx="11" cy="20" r="1.6"/><circle cx="19" cy="20" r="1.6"/>'),
    'georgian': _i('<rect x="4" y="4" width="22" height="22" rx="2"/><path d="M11.3 4v22M18.6 4v22M4 15h22"/>'),
    'igu': _i('<rect x="4" y="6" width="9" height="18" rx="1"/><rect x="17" y="6" width="9" height="18" rx="1"/><path d="M13 15h4"/>'),
    'po': _i('<path d="M6 4h13l5 5v17H6z"/><path d="M10 13h10M10 17h10M10 21h6"/>'),
    'ipad': _i('<rect x="5" y="4" width="20" height="22" rx="3"/><path d="M10 10h10M10 15h6"/><path d="M15 20l3 3 5-6"/>'),
    'orders': _i('<rect x="6" y="5" width="18" height="21" rx="2"/><path d="M11 5V3h8v2M10 12h10M10 16h10M10 20h6"/>'),
    'quote': _i('<path d="M7 4h11l5 5v17H7z"/><path d="M11 14h8M11 18h8"/><path d="M15 9.5v-0"/>'),
    'invoice': _i('<path d="M7 4h16v22l-3-2-3 2-2-2-3 2-2-2-3 2z"/><path d="M11 10h8M11 14h8M11 18h5"/>'),
    'survey': _i('<rect x="8" y="3" width="14" height="24" rx="3"/><path d="M12 9h6M12 13h6M12 17h3"/>'),
    'production': _i('<rect x="4" y="5" width="6" height="20" rx="1"/><rect x="12" y="5" width="6" height="14" rx="1"/><rect x="20" y="5" width="6" height="9" rx="1"/>'),
    'schedule': _i('<rect x="4" y="6" width="22" height="20" rx="2"/><path d="M4 12h22M10 3v6M20 3v6M9 17h4M9 21h8"/>'),
    'chat': _i('<path d="M5 6h20v14H13l-6 5v-5H5z"/><path d="M10 12h10M10 15h6"/>'),
    'fitting': _i('<path d="M5 25h20"/><rect x="7" y="5" width="16" height="16" rx="1"/><path d="M11 13l3 3 6-6"/>'),
    'webshop': _i('<path d="M5 7h3l3 13h12l2-9H10"/><circle cx="13" cy="24" r="1.6"/><circle cx="21" cy="24" r="1.6"/>'),
    'fleet': _i('<path d="M3 20V9h14v11M17 13h5l4 4v3h-9"/><circle cx="8" cy="21" r="2.4"/><circle cx="21" cy="21" r="2.4"/>'),
    'mobile': _i('<rect x="9" y="3" width="12" height="24" rx="3"/><path d="M13.5 23h3"/>'),
    'counter': _i('<path d="M4 13h22v12H4z"/><path d="M6 13l3-7h12l3 7M12 19h6"/>'),
    'merchant': _i('<path d="M4 25V11l11-6 11 6v14"/><path d="M9 25v-8h12v8M9 21h12"/>'),
    'glazier': _i('<path d="M5 25V8h20v17"/><path d="M15 8v17M5 16h20"/><path d="M3 25h24"/>'),
    'processor': _i('<circle cx="15" cy="15" r="9"/><circle cx="15" cy="15" r="3"/><path d="M15 3v3M15 24v3M3 15h3M24 15h3"/>'),
}
