import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

class ZeroMail(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Mail - Ultimate Studio")
        self.set_default_size(1350, 850)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= SIDEBAR =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_size_request(240, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        logo = Gtk.Label(label="Z E R O M A I L")
        logo.get_style_context().add_class("sidebar-logo")
        logo_box.pack_start(logo, True, True, 0)
        self.sidebar.pack_start(logo_box, False, False, 20)
        
        btn_compose = Gtk.Button(label="✏️ Compose")
        btn_compose.get_style_context().add_class("action-btn")
        self.sidebar.pack_start(btn_compose, False, False, 10)
        
        lbl_folders = Gtk.Label(label="FOLDERS")
        lbl_folders.get_style_context().add_class("section-label")
        lbl_folders.set_halign(Gtk.Align.START)
        lbl_folders.set_margin_start(20)
        lbl_folders.set_margin_top(15)
        self.sidebar.pack_start(lbl_folders, False, False, 10)
        
        folders = ["📥 Inbox", "⭐ Starred", "📤 Sent", "📝 Drafts", "🗑️ Trash"]
        for f in folders:
            btn = Gtk.Button(label=f)
            btn.get_style_context().add_class("folder-btn")
            btn.set_alignment(0.0, 0.5)
            self.sidebar.pack_start(btn, False, False, 2)
            
        # ================= INBOX LIST =================
        self.inbox_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.inbox_box.set_size_request(350, -1)
        self.inbox_box.get_style_context().add_class("inbox-col")
        main_box.pack_start(self.inbox_box, False, False, 0)
        
        search_entry = Gtk.Entry()
        search_entry.set_placeholder_text("🔍 Search Mail...")
        search_entry.get_style_context().add_class("search-entry")
        search_entry.set_margin_top(15)
        search_entry.set_margin_start(15)
        search_entry.set_margin_end(15)
        search_entry.set_margin_bottom(15)
        self.inbox_box.pack_start(search_entry, False, False, 0)
        
        scroll_inbox = Gtk.ScrolledWindow()
        self.inbox_list = Gtk.ListBox()
        self.inbox_list.get_style_context().add_class("transparent-list")
        
        emails = [
            ("GitHub", "New push to main", "You successfully pushed 5 commits..."),
            ("Studio Team", "Welcome to Zero", "Thanks for installing the ultimate suite..."),
            ("Security", "New Sign-in", "We noticed a new login on Arch Linux..."),
            ("Newsletter", "Weekly Trends", "Top UI designs of September 2026..."),
            ("Billing", "Invoice #892", "Your recent transaction has been processed...")
        ]
        
        for sender, subj, preview in emails:
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("mail-row")
            
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            vbox.set_margin_start(15)
            vbox.set_margin_end(15)
            vbox.set_margin_top(12)
            vbox.set_margin_bottom(12)
            
            lbl_sender = Gtk.Label(label=sender)
            lbl_sender.set_halign(Gtk.Align.START)
            lbl_sender.get_style_context().add_class("mail-sender")
            
            lbl_subj = Gtk.Label(label=subj)
            lbl_subj.set_halign(Gtk.Align.START)
            lbl_subj.get_style_context().add_class("mail-subj")
            
            lbl_prev = Gtk.Label(label=preview)
            lbl_prev.set_halign(Gtk.Align.START)
            lbl_prev.get_style_context().add_class("mail-prev")
            lbl_prev.set_ellipsize(3)
            
            vbox.pack_start(lbl_sender, False, False, 0)
            vbox.pack_start(lbl_subj, False, False, 0)
            vbox.pack_start(lbl_prev, False, False, 0)
            row.add(vbox)
            self.inbox_list.add(row)
            
        scroll_inbox.add(self.inbox_list)
        self.inbox_box.pack_start(scroll_inbox, True, True, 0)
        
        # ================= READING PANE =================
        self.read_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.read_pane.get_style_context().add_class("read-pane")
        main_box.pack_start(self.read_pane, True, True, 0)
        
        mail_header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        mail_header.set_margin_top(30)
        mail_header.set_margin_start(40)
        mail_header.set_margin_end(40)
        mail_header.set_margin_bottom(20)
        
        h_subj = Gtk.Label(label="Welcome to Zero")
        h_subj.set_halign(Gtk.Align.START)
        h_subj.get_style_context().add_class("read-subj")
        
        h_sender = Gtk.Label(label="From: Studio Team <hello@studio.local>")
        h_sender.set_halign(Gtk.Align.START)
        h_sender.get_style_context().add_class("read-sender")
        
        mail_header.pack_start(h_subj, False, False, 0)
        mail_header.pack_start(h_sender, False, False, 0)
        self.read_pane.pack_start(mail_header, False, False, 0)
        
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_start(40)
        sep.set_margin_end(40)
        self.read_pane.pack_start(sep, False, False, 0)
        
        mail_body = Gtk.TextView()
        mail_body.set_wrap_mode(Gtk.WrapMode.WORD)
        mail_body.set_left_margin(40)
        mail_body.set_right_margin(40)
        mail_body.set_top_margin(20)
        mail_body.get_style_context().add_class("read-body")
        mail_body.set_editable(False)
        mail_body.get_buffer().set_text(
            "Hello,\n\n"
            "Thank you for installing the Ultimate Studio suite.\n"
            "Your workspace is now upgraded with premium radial glassmorphism UI designs.\n\n"
            "Enjoy the lightning fast, secure experience.\n\n"
            "Best,\nStudio Team"
        )
        
        scroll_body = Gtk.ScrolledWindow()
        scroll_body.add(mail_body)
        self.read_pane.pack_start(scroll_body, True, True, 0)
        
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .sidebar { background-color: rgba(6, 8, 12, 0.98); border-right: 1px solid rgba(255, 255, 255, 0.03); }
            .sidebar-logo { color: #FFFFFF; font-size: 20px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(255, 170, 0, 0.6); }
            .action-btn { background: linear-gradient(45deg, #FFaa00, #FF6600); color: #000000; border-radius: 12px; font-weight: bold; padding: 12px; margin: 0 20px; border: none; box-shadow: 0 5px 15px rgba(255, 170, 0, 0.3); transition: all 0.3s; }
            .action-btn:hover { box-shadow: 0 8px 25px rgba(255, 170, 0, 0.5); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .folder-btn { background: transparent; color: #8B94A5; border: none; box-shadow: none; padding: 10px 20px; font-size: 14px; font-weight: bold; }
            .folder-btn:hover { background: rgba(255, 255, 255, 0.05); color: #FFFFFF; border-radius: 8px; }
            .inbox-col { background-color: #080A10; border-right: 1px solid rgba(255, 255, 255, 0.05); }
            .search-entry { background: #10141E; color: #FFFFFF; border: 1px solid #1C2333; border-radius: 10px; padding: 10px; box-shadow: none; }
            .transparent-list { background: transparent; }
            .mail-row { background: transparent; border-bottom: 1px solid rgba(255,255,255,0.03); transition: all 0.2s; }
            .mail-row:hover { background: rgba(255, 255, 255, 0.03); cursor: pointer; }
            .mail-row:selected { background: rgba(255, 170, 0, 0.1); border-left: 3px solid #FFaa00; }
            .mail-sender { color: #FFFFFF; font-weight: bold; font-size: 14px; }
            .mail-subj { color: #8B94A5; font-size: 13px; font-weight: bold; }
            .mail-prev { color: #4A5568; font-size: 12px; }
            .read-pane { background: radial-gradient(circle at top right, #0A0D14, #030305); }
            .read-subj { color: #FFFFFF; font-size: 28px; font-weight: bold; }
            .read-sender { color: #8B94A5; font-size: 14px; }
            .read-body { background: transparent; color: #c9d1d9; font-size: 16px; line-height: 1.6; }
            .read-body text { background: transparent; }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroMail()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
