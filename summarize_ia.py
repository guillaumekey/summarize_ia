import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Générateur de boutons de résumé IA",
    page_icon="https://www.google.com/s2/favicons?sz=64&domain_url=https%3A%2F%2Fwww.keyweo.com%2Ffr%2F",
    layout="wide",
)

# Import translations
from translations import translations

# CSS for styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: #6FC7A1;
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.code-container {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Sidebar with logo and navigation
with st.sidebar:
    # Keyweo Logo
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
        <img src="https://www.keyweo.com/wp-content/uploads/2021/11/keyweo-logo.webp" 
             alt="Keyweo Logo" 
             style="height: 50px; width: auto;">
    </div>
    """, unsafe_allow_html=True)

    # Language selection
    language = st.selectbox(
        "",
        ["Français", "English", "Español", "Deutsch", "Italiano", "Nederlands"],
        index=0,
        label_visibility="collapsed"
    )

# Get translations once
t = translations[language]

# Update sidebar with translations
with st.sidebar:
    # Separator
    st.markdown("---")

    # Navigation links
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <a href="{t['site_url']}" target="_blank" 
           style="display: block; padding: 0.5rem; text-decoration: none; color: #121212; font-weight: 500; margin-bottom: 0.5rem;">
           {t['access_site']}
        </a>
        <a href="{t['contact_url']}" target="_blank"
           style="display: block; padding: 0.5rem; text-decoration: none; color: #121212; font-weight: 500;">
           {t['contact_us']}
        </a>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown(f"""
<div class="main-header">
    <h1>{t['title']}</h1>
    <p>{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)


# Helper function to get selected services
def get_selected_services(include_perplexity, include_chatgpt, include_google, include_grok,
                          text_perplexity, text_chatgpt, text_google, text_grok,
                          color_perplexity, color_chatgpt, color_google, color_grok,
                          text_color_perplexity, text_color_chatgpt, text_color_google, text_color_grok):
    services = []
    if include_perplexity:
        services.append(('perplexity', text_perplexity, color_perplexity, text_color_perplexity))
    if include_chatgpt:
        services.append(('chatgpt', text_chatgpt, color_chatgpt, text_color_chatgpt))
    if include_google:
        services.append(('google', text_google, color_google, text_color_google))
    if include_grok:
        services.append(('grok', text_grok, color_grok, text_color_grok))
    return services


# Generate CSS for buttons
def generate_button_css(container_bg_color, container_border_radius, border_style, title_color, padding_value):
    return f"""
#summary-shortcut{{margin:0 auto;}}
#summary-shortcut .ss-box{{padding:24px;background:{container_bg_color};border-radius:{container_border_radius}px;{border_style}box-shadow:0 2px 10px rgba(0,0,0,0.1);}}
#summary-shortcut .ss-title{{font-weight:700;text-align:center;margin:0 0 1rem;color:{title_color};}}
#summary-shortcut .ss-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;}}
#summary-shortcut button{{width:100%;padding:{padding_value}px 16px;font-weight:600;color:#fff;border:none;cursor:pointer;transition:all .2s ease;}}
#summary-shortcut button:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.2);}}
"""


# Generate JavaScript providers
def generate_js_providers(services, t):
    provider_entries = []
    service_configs = {
        'perplexity': "return 'https://www.perplexity.ai/search/new?q='+encodeURIComponent(finalPrompt);",
        'chatgpt': """var q = encodeURIComponent(finalPrompt);
      var ts = Date.now();
      return 'https://chatgpt.com/?q=' + q + '&ts=' + ts + '#q=' + q + '&ts2=' + ts;""",
        'google': "return 'https://www.google.com/search?udm=50&aep=11&q='+encodeURIComponent(finalPrompt);",
        'grok': "return 'https://x.com/i/grok?text='+encodeURIComponent(finalPrompt);"
    }

    for service_id, _, _, _ in services:
        if service_id in service_configs:
            provider_entries.append(f"""{service_id}:function(u){{
      var domain = new URL(u).hostname;
      var finalPrompt = PROMPT.replace('{t['url_placeholder']}', u).replace('{t['site_placeholder']}', domain);
      {service_configs[service_id]}
    }}""")

    return "var PROVIDERS={" + ",\n    ".join(provider_entries) + "\n  };"


# Main function to generate complete code
def generate_code(border_radius_value, padding_value, services, title_text, title_color, custom_prompt,
                  container_border_radius, container_bg_color, border_style):
    # Generate HTML buttons
    buttons_html = "".join([
        f'<button class="btn-{service_id}" data-provider="{service_id}" '
        f'style="background:{bg_color};color:{text_color};border-radius:{border_radius_value}px">'
        f'{service_text}</button>'
        for service_id, service_text, bg_color, text_color in services
    ])

    # Generate CSS
    css = generate_button_css(container_bg_color, container_border_radius, border_style, title_color, padding_value)

    # Generate JavaScript
    js_providers = generate_js_providers(services, t)
    clean_prompt = custom_prompt.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')

    return f"""<!-- 🔽 AI Summary Button Block -->
<style>
{css}
</style>

<div id="summary-shortcut">
  <div class="ss-box">
    <p class="ss-title">{title_text}</p>
    <div class="ss-grid">
      {buttons_html}
    </div>
  </div>
</div>

<script>
(function(){{
  var PROMPT='{clean_prompt} ';
  {js_providers}

  function getArticleUrl(){{
    var canon=document.querySelector('link[rel="canonical"]');
    return (canon && canon.href)? canon.href : window.location.href;
  }}

  document.querySelectorAll('#summary-shortcut button').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      var p=btn.dataset.provider;
      if(!PROVIDERS[p]) return;
      var u=getArticleUrl();
      var target=PROVIDERS[p](u);
      var winName = (p==='chatgpt') ? ('chatgpt_'+Date.now()) : '_blank';
      window.open(target, winName, 'noopener,noreferrer');
    }}, {{passive:true}});
  }});
}})();
</script>
<!-- 🔼 End of AI Summary Button Block -->"""


# Function to generate optimized code with separate CSS
def generate_optimized_code(border_radius_value, padding_value, services, title_text, title_color, custom_prompt,
                            container_border_radius, container_bg_color, border_style, t):
    # Generate CSS for separate file
    button_styles = ""
    for service_id, _, bg_color, _ in services:
        button_styles += f"#summary-shortcut .btn-{service_id}{{background:{bg_color};}}\n"

    css_code = f"""/* AI Summary Buttons CSS - Add to your style.css file */
#summary-shortcut{{margin:0 auto;}}
#summary-shortcut .ss-box{{padding:24px;background:{container_bg_color};border-radius:{container_border_radius}px;{border_style}box-shadow:0 2px 10px rgba(0,0,0,0.1);}}
#summary-shortcut .ss-title{{font-weight:700;text-align:center;margin:0 0 1rem;color:{title_color};}}
#summary-shortcut .ss-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;}}
#summary-shortcut button{{width:100%;padding:{padding_value}px 16px;font-weight:600;color:#fff;border:none;cursor:pointer;transition:all .2s ease;border-radius:{border_radius_value}px;}}
#summary-shortcut button:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.2);}}
{button_styles.rstrip()}"""

    # Generate HTML+JS without inline styles
    buttons_html = ""
    for service_id, service_text, _, _ in services:
        buttons_html += f'      <button class="btn-{service_id}" data-provider="{service_id}">{service_text}</button>\n'

    js_providers = generate_js_providers(services, t)
    clean_prompt = custom_prompt.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')

    step1_title = t.get('css_block_title', '=== ÉTAPE 1: CSS À AJOUTER DANS VOTRE FICHIER STYLE.CSS ===')
    step2_title = t.get('html_block_title', '=== ÉTAPE 2: HTML + JAVASCRIPT À UTILISER DANS VOS ARTICLES ===')

    html_js_code = f"""{step1_title}

{css_code}

{step2_title}

<!-- 🔽 AI Summary Button Block - HTML + JavaScript -->
<div id="summary-shortcut">
  <div class="ss-box">
    <p class="ss-title">{title_text}</p>
    <div class="ss-grid">
{buttons_html.rstrip()}
    </div>
  </div>
</div>

<script>
(function(){{
  var PROMPT='{clean_prompt} ';
  {js_providers}

  function getArticleUrl(){{
    var canon=document.querySelector('link[rel="canonical"]');
    return (canon && canon.href)? canon.href : window.location.href;
  }}

  document.querySelectorAll('#summary-shortcut button').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      var p=btn.dataset.provider;
      if(!PROVIDERS[p]) return;
      var u=getArticleUrl();
      var target=PROVIDERS[p](u);
      var winName = (p==='chatgpt') ? ('chatgpt_'+Date.now()) : '_blank';
      window.open(target, winName, 'noopener,noreferrer');
    }}, {{passive:true}});
  }});
}})();
</script>
<!-- 🔼 End of AI Summary Button Block -->

=== {t.get('instructions_label', 'INSTRUCTIONS D\'INSTALLATION')} ===

1. Copiez le CSS (ÉTAPE 1) dans votre fichier style.css ou dans l'éditeur de thème WordPress
2. Collez le HTML+JavaScript (ÉTAPE 2) dans vos articles où vous voulez afficher les boutons
3. Le CSS sera chargé une seule fois pour tout votre site

AVANTAGES DE CETTE MÉTHODE :
✓ Performances optimisées (CSS mis en cache par le navigateur)
✓ Maintenance simplifiée (modification du style en un seul endroit)
✓ Code HTML plus propre et professionnel
✓ Cohérence visuelle garantie sur tout le site"""

    return html_js_code


# Button configuration
with st.expander(t['config_button'], expanded=True):
    col_config1, col_config2 = st.columns(2)

    with col_config1:
        # Title configuration
        st.markdown(t['block_title'])
        col_title_text, col_title_color = st.columns([4, 0.6])
        with col_title_text:
            title_text = st.text_input("", value=t['default_title'], help=t['title_help'], label_visibility="collapsed")
        with col_title_color:
            title_color = st.color_picker("", "#2D3748", help=t['title_color_help'], label_visibility="collapsed",
                                          key="title_color")

        # Button styling
        st.markdown(t['border_radius'])
        border_radius_value = st.slider("", 0, 50, 8, 1, help=t['border_help'], label_visibility="collapsed")

        st.markdown(t['button_thickness'])
        padding_value = st.slider("", 8, 30, 12, 1, help=t['thickness_help'], label_visibility="collapsed")

    with col_config2:
        # AI services configuration
        st.markdown(t['ai_services'])

        # Service configurations (could be further optimized with a loop)
        services_config = [
            ('perplexity', 'Perplexity', t['perplexity_text'], '#21808D'),
            ('chatgpt', 'ChatGPT', t['chatgpt_text'], '#10A37F'),
            ('google', 'Google AI', t['google_text'], '#DB4437'),
            ('grok', 'Grok', t['grok_text'], '#000000')
        ]

        service_vars = {}
        for service_key, service_name, default_text, default_color in services_config:
            cols = st.columns([1.5, 2.5, 1, 1])
            with cols[0]:
                service_vars[f'include_{service_key}'] = st.checkbox(service_name, value=True)
            with cols[1]:
                service_vars[f'text_{service_key}'] = st.text_input("", value=default_text, key=f"text_{service_key}",
                                                                    label_visibility="collapsed")
            with cols[2]:
                service_vars[f'color_{service_key}'] = st.color_picker("", default_color, key=f"color_{service_key}",
                                                                       label_visibility="collapsed",
                                                                       help=t['bg_color_help'])
            with cols[3]:
                service_vars[f'text_color_{service_key}'] = st.color_picker("", "#FFFFFF",
                                                                            key=f"text_color_{service_key}",
                                                                            label_visibility="collapsed",
                                                                            help=t['text_color_help'])

    # Prompt configuration
    st.markdown(t['custom_prompt'])
    custom_prompt = st.text_area("", value=t['default_prompt'], height=80, help=t['prompt_help'],
                                 label_visibility="collapsed")

    # Container styling
    st.markdown("---")
    st.markdown(t['container_style'])

    col_container1, col_container2, col_container3 = st.columns(3)
    with col_container1:
        st.markdown(t['container_radius'])
        container_border_radius = st.slider("", 0, 30, 12, 1, help=t['container_radius_help'],
                                            label_visibility="collapsed", key="container_radius")

    with col_container2:
        st.markdown(t['container_bg'])
        container_bg_color = st.color_picker("", "#FFFFFF", help=t['container_bg_help'], label_visibility="collapsed",
                                             key="container_bg")

    with col_container3:
        st.markdown(t['container_border'])
        enable_border = st.checkbox(t['enable_border'], value=False, key="enable_border")
        if enable_border:
            border_color = st.color_picker("", "#E2E8F0", help=t['border_color_help'], label_visibility="collapsed",
                                           key="border_color")
            border_width = st.slider("", 1, 5, 2, 1, help=t['border_width_help'], label_visibility="collapsed",
                                     key="border_width")
        else:
            border_color, border_width = "#E2E8F0", 0

# Get selected services for preview and code generation
services = get_selected_services(
    service_vars['include_perplexity'], service_vars['include_chatgpt'],
    service_vars['include_google'], service_vars['include_grok'],
    service_vars['text_perplexity'], service_vars['text_chatgpt'],
    service_vars['text_google'], service_vars['text_grok'],
    service_vars['color_perplexity'], service_vars['color_chatgpt'],
    service_vars['color_google'], service_vars['color_grok'],
    service_vars['text_color_perplexity'], service_vars['text_color_chatgpt'],
    service_vars['text_color_google'], service_vars['text_color_grok']
)

# Preview section with functional buttons
st.header(t['real_preview'])
border_style = f"border:{border_width}px solid {border_color};" if enable_border and border_width > 0 else ""

# Add URL input for testing
test_url = st.text_input(
    t['test_url_label'],
    value="https://www.keyweo.com/fr/",
    placeholder="Entrez l'URL d'un article à tester",
    help=t['test_url_help']
)

preview_css = f"""
<style>
.preview-container {{
    padding: 24px;
    background: {container_bg_color};
    border-radius: {container_border_radius}px;
    {border_style}
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    max-width: 800px;
    margin: 0 auto;
}}
.preview-title {{
    font-weight: 700;
    text-align: center;
    margin: 0 0 1rem;
    color: {title_color};
    font-size: 1.1em;
}}
.preview-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
}}
.preview-button {{
    width: 100%;
    padding: {padding_value}px 16px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all .2s ease;
    border-radius: {border_radius_value}px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    text-decoration: none !important;
    display: inline-block;
    text-align: center;
}}
.preview-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    text-decoration: none !important;
}}
</style>
"""

# Generate functional preview buttons
preview_buttons_html = ""
for service_id, service_text, bg_color, text_color in services:
    try:
        from urllib.parse import urlparse, quote_plus

        domain = urlparse(test_url).netloc
    except:
        domain = "example.com"

    # Create the prompt with URL and domain replacement
    test_prompt = custom_prompt.replace(t['url_placeholder'], test_url).replace(t['site_placeholder'], domain)
    encoded_prompt = quote_plus(test_prompt)

    if service_id == 'perplexity':
        test_link = f"https://www.perplexity.ai/search/new?q={encoded_prompt}"
    elif service_id == 'chatgpt':
        import time

        ts = int(time.time() * 1000)
        test_link = f"https://chatgpt.com/?q={encoded_prompt}&ts={ts}#q={encoded_prompt}&ts2={ts}"
    elif service_id == 'google':
        test_link = f"https://www.google.com/search?udm=50&aep=11&q={encoded_prompt}"
    elif service_id == 'grok':
        test_link = f"https://x.com/i/grok?text={encoded_prompt}"
    else:
        test_link = "#"

    preview_buttons_html += f'''
    <a href="{test_link}" target="_blank" class="preview-button" 
       style="background-color: {bg_color}; color: {text_color};">
       {service_text}
    </a>'''

st.markdown(f"""
{preview_css}
<div class="preview-container">
    <p class="preview-title">{title_text}</p>
    <div class="preview-grid">{preview_buttons_html}</div>
</div>
""", unsafe_allow_html=True)

if test_url:
    st.info(t['functional_buttons_info'])

st.markdown("---")

# Code generation
st.header(t['generated_code'])

# Add option to choose code format
code_format = st.radio(
    t['code_format'],
    [t['code_complete'], t['code_optimized']],
    help=t.get('optimization_recommendation', 'Le code optimisé sépare le CSS pour de meilleures performances')
)

if code_format == t['code_optimized']:
    st.info(t['optimization_recommendation'])

if st.button(t['generate_code'], type="primary"):
    if code_format == t['code_complete']:
        code = generate_code(border_radius_value, padding_value, services, title_text, title_color,
                             custom_prompt, container_border_radius, container_bg_color, border_style)
    else:
        code = generate_optimized_code(border_radius_value, padding_value, services, title_text, title_color,
                                       custom_prompt, container_border_radius, container_bg_color, border_style, t)

    st.session_state.generated_code = code
    st.session_state.code_format = code_format

if 'generated_code' in st.session_state:
    code_format_used = st.session_state.get('code_format', t['code_complete'])

    if code_format_used == t['code_optimized']:
        # Split CSS and HTML for separate display
        full_code = st.session_state.generated_code

        # Extract CSS part (between the CSS comment and before HTML)
        css_start = full_code.find("/* AI Summary Buttons CSS")
        html_marker = full_code.find(t.get('html_block_title', '=== ÉTAPE 2:'))
        css_end = html_marker if html_marker != -1 else full_code.find("<!-- 🔽 AI Summary Button Block")

        if css_start != -1 and css_end != -1:
            css_code = full_code[css_start:css_end].strip()
        else:
            css_code = "Erreur d'extraction CSS"

        # Extract HTML part
        html_start = full_code.find("<!-- 🔽 AI Summary Button Block")
        html_end = full_code.find("<!-- 🔼 End of AI Summary Button Block -->")
        if html_end != -1:
            html_end = html_end + len("<!-- 🔼 End of AI Summary Button Block -->")

        if html_start != -1 and html_end != -1:
            html_code = full_code[html_start:html_end].strip()
        else:
            html_code = "Erreur d'extraction HTML"

        st.info(f"""
        {t['instructions_label']}
        {t.get('css_step', '1. Copiez le CSS du premier bloc dans votre fichier style.css')}
        {t.get('html_step', '2. Copiez le HTML+JavaScript du second bloc dans vos articles')}
        """)

        # CSS Block
        st.subheader(t['css_block_title'])
        st.markdown('<div class="code-container">', unsafe_allow_html=True)
        st.code(css_code, language="css")
        st.markdown('</div>', unsafe_allow_html=True)

        # HTML Block
        st.subheader(t['html_block_title'])
        st.markdown('<div class="code-container">', unsafe_allow_html=True)
        st.code(html_code, language="html")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="code-container">', unsafe_allow_html=True)
        st.code(st.session_state.generated_code, language="html")
        st.markdown('</div>', unsafe_allow_html=True)

    # Different filename based on format
    filename = "bouton_resume_ia_optimise.html" if code_format_used == t['code_optimized'] else "bouton_resume_ia.html"

    st.download_button(
        label=t['download_code'],
        data=st.session_state.generated_code,
        file_name=filename,
        mime="text/html"
    )
else:
    st.info(t['click_generate'])

# Instructions
st.markdown("---")
with st.expander(t['usage_instructions']):
    st.markdown(f"""
    {t['how_to_integrate']}
    {t['step1']}
    {t['step2']}
    {t['step3']}
    {t['step4']}
    {t['step5']}
    {t['step6']}

    {t['how_it_works']}
    {t['works1']}
    {t['works2']}
    {t['works3']}

    {t['support']}
    {t['support_text']}
    """)

# Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center; color: #666; padding: 1rem;"><p>{t["footer"]}</p></div>',
            unsafe_allow_html=True)