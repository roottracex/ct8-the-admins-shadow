from flask import (
    Flask,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    render_template_string
)

app = Flask(__name__)
app.secret_key = "cybertec8-ctf-secret-key"


# ============================================================
# RESOURCE DATA
# ============================================================

RESOURCES = {
    101: {
        "title": "Security Documentation",
        "classification": "INTERNAL",
        "content": "Standard security procedures for Cybertec8 employees."
    },

    202: {
        "title": "Application Security Review",
        "classification": "INTERNAL",
        "content": "Quarterly application security review."
    },

    303: {
        "title": "Administrative Security Report",
        "classification": "RESTRICTED",
        "content": "Administrative security information.",
        "flag": "Flag_CT8{admin_shadow_exposed}"
    }
}


# ============================================================
# COMMON PAGE
# ============================================================

def page(title, content):

    return f"""
    <!DOCTYPE html>
    <html>
    <head>

        <title>{title} | Cybertec8</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                background: #070b14;
                color: #e6edf7;
                font-family: Arial, Helvetica, sans-serif;
            }}

            .layout {{
                display: flex;
                min-height: 100vh;
            }}

            .sidebar {{
                width: 240px;
                background: #0b111d;
                border-right: 1px solid #1c2a3d;
                padding: 25px 18px;
            }}

            .logo {{
                font-size: 22px;
                font-weight: bold;
                color: #38bdf8;
                margin-bottom: 35px;
            }}

            .logo span {{
                color: white;
            }}

            .nav a {{
                display: block;
                padding: 13px 14px;
                margin-bottom: 8px;
                color: #94a3b8;
                text-decoration: none;
                border-radius: 8px;
            }}

            .nav a:hover {{
                background: #111c2d;
                color: #38bdf8;
            }}

            .main {{
                flex: 1;
            }}

            .topbar {{
                height: 65px;
                border-bottom: 1px solid #1c2a3d;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 30px;
                background: #080e19;
            }}

            .status {{
                color: #4ade80;
                font-size: 13px;
            }}

            .container {{
                padding: 40px;
                max-width: 1100px;
            }}

            h1 {{
                margin-top: 0;
                font-size: 30px;
            }}

            .subtitle {{
                color: #94a3b8;
                margin-bottom: 30px;
            }}

            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 20px;
            }}

            .card {{
                background: #0d1422;
                border: 1px solid #203047;
                border-radius: 12px;
                padding: 24px;
            }}

            .card h3 {{
                margin-top: 0;
            }}

            .badge {{
                display: inline-block;
                padding: 5px 9px;
                border-radius: 5px;
                font-size: 11px;
                margin-bottom: 15px;
                background: #132337;
                color: #38bdf8;
            }}

            .restricted {{
                color: #f87171;
            }}

            .btn {{
                display: inline-block;
                margin-top: 15px;
                padding: 10px 15px;
                background: #0ea5e9;
                color: white;
                text-decoration: none;
                border-radius: 7px;
                font-size: 14px;
            }}

            .btn:hover {{
                background: #0284c7;
            }}

            .denied {{
                max-width: 550px;
                margin: 100px auto;
                text-align: center;
                background: #0d1422;
                border: 1px solid #26364d;
                border-radius: 14px;
                padding: 45px;
                box-shadow: 0 20px 60px rgba(0,0,0,.4);
            }}

            .denied-icon {{
                font-size: 48px;
                margin-bottom: 15px;
            }}

            .denied h1 {{
                color: #ff5c5c;
            }}

            .denied p {{
                color: #94a3b8;
                line-height: 1.6;
            }}

            .code {{
                margin-top: 25px;
                padding: 12px;
                background: #080d17;
                border-radius: 8px;
                color: #64748b;
                font-family: monospace;
                font-size: 13px;
            }}

            .login {{
                width: 400px;
                margin: 120px auto;
                background: #0d1422;
                border: 1px solid #203047;
                border-radius: 14px;
                padding: 35px;
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin: 8px 0 15px;
                background: #080e19;
                border: 1px solid #26364d;
                border-radius: 7px;
                color: white;
            }}

            button {{
                width: 100%;
                padding: 12px;
                border: 0;
                border-radius: 7px;
                background: #0ea5e9;
                color: white;
                cursor: pointer;
            }}

            button:hover {{
                background: #0284c7;
            }}

        </style>

    </head>

    <body>

        <div class="layout">

            <aside class="sidebar">

                <div class="logo">
                    CYBERTEC<span>8</span>
                </div>

                <div class="nav">

                    <a href="/">Dashboard</a>
                    <a href="/profile">My Profile</a>
                    <a href="/reports">Security Reports</a>
                    <a href="/access">Access Center</a>

                </div>

            </aside>


            <main class="main">

                <div class="topbar">

                    <div>
                        Cybertec8 Internal Security Portal
                    </div>

                    <div class="status">
                        ● SYSTEM OPERATIONAL
                    </div>

                </div>

                <div class="container">

                    {content}

                </div>

            </main>

        </div>

    </body>
    </html>
    """


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "employee" and password == "cybertec8":

            session["username"] = username
            session["role"] = "employee"

            return redirect(url_for("dashboard"))

        return """
        <h2>Invalid credentials</h2>
        <a href="/login">Back to login</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>

        <title>Login | Cybertec8</title>

        <style>

            body {
                background:#070b14;
                color:white;
                font-family:Arial;
            }

            .login {
                width:400px;
                margin:120px auto;
                background:#0d1422;
                padding:35px;
                border-radius:14px;
                border:1px solid #203047;
            }

            input {
                width:100%;
                padding:12px;
                margin:8px 0 15px;
                background:#080e19;
                border:1px solid #26364d;
                border-radius:7px;
                color:white;
                box-sizing:border-box;
            }

            button {
                width:100%;
                padding:12px;
                background:#0ea5e9;
                color:white;
                border:0;
                border-radius:7px;
                cursor:pointer;
            }

            h1 {
                color:#38bdf8;
            }

        </style>

    </head>

    <body>

        <div class="login">

            <h1>CYBERTEC8</h1>

            <p>Internal Security Portal</p>

            <form method="POST">

                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    required
                >

                <button type="submit">
                    Sign In
                </button>

            </form>

        </div>

    </body>
    </html>
    """


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    content = """

    <h1>Security Dashboard</h1>

    <div class="subtitle">
        Welcome to the Cybertec8 internal security environment.
    </div>

    <div class="cards">

        <div class="card">
            <span class="badge">SYSTEM</span>
            <h3>Security Status</h3>
            <p>All internal services are operational.</p>
        </div>

        <div class="card">
            <span class="badge">ACCESS</span>
            <h3>Access Center</h3>
            <p>Review available internal resources.</p>
            <a class="btn" href="/access">
                Open Access Center
            </a>
        </div>

        <div class="card">
            <span class="badge">REPORTS</span>
            <h3>Security Reports</h3>
            <p>Review internal security reports.</p>
            <a class="btn" href="/reports">
                View Reports
            </a>
        </div>

    </div>

    """

    return page("Dashboard", content)


# ============================================================
# PROFILE
# ============================================================

@app.route("/profile")
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    content = f"""

    <h1>My Profile</h1>

    <div class="subtitle">
        Employee account information.
    </div>

    <div class="card">

        <h3>Employee Account</h3>

        <p>
            <strong>Username:</strong>
            {session.get("username")}
        </p>

        <p>
            <strong>Access Level:</strong>
            Employee
        </p>

        <p>
            <strong>Status:</strong>
            Active
        </p>

    </div>

    """

    return page("Profile", content)


# ============================================================
# SECURITY REPORTS
# ============================================================

@app.route("/reports")
def reports():

    if "username" not in session:
        return redirect(url_for("login"))

    content = """

    <h1>Security Reports</h1>

    <div class="subtitle">
        Internal security monitoring and reports.
    </div>

    <div class="cards">

        <div class="card">
            <span class="badge">INTERNAL</span>
            <h3>Application Security Review</h3>
            <p>Quarterly application security review.</p>
        </div>

        <div class="card">
            <span class="badge">INTERNAL</span>
            <h3>Security Documentation</h3>
            <p>Standard security procedures.</p>
        </div>

    </div>

    """

    return page("Reports", content)


# ============================================================
# ACCESS CENTER
# ============================================================

@app.route("/access")
def access():

    if "username" not in session:
        return redirect(url_for("login"))

    content = """

    <h1>Access Center</h1>

    <div class="subtitle">
        Internal resources available to your current access level.
    </div>

    <div class="cards">

        <div class="card">

            <span class="badge">
                INTERNAL
            </span>

            <h3>
                Security Documentation
            </h3>

            <p>
                Standard security procedures.
            </p>

            <a
                class="btn"
                href="/resource/101"
            >
                Open Resource
            </a>

        </div>


        <div class="card">

            <span class="badge">
                INTERNAL
            </span>

            <h3>
                Application Security Review
            </h3>

            <p>
                Quarterly application security review.
            </p>

            <a
                class="btn"
                href="/resource/202"
            >
                Open Resource
            </a>

        </div>


        <div class="card">

            <span class="badge restricted">
                RESTRICTED
            </span>

            <h3>
                Administrative Security Report
            </h3>

            <p>
                Administrative security information.
            </p>

            <a
                class="btn"
                href="/resource/303"
            >
                Open Resource
            </a>

        </div>

    </div>

    """

    return page("Access Center", content)


# ============================================================
# RESOURCE PAGE
# ============================================================

@app.route("/resource/<int:resource_id>")
def resource(resource_id):

    if "username" not in session:
        return redirect(url_for("login"))

    resource_data = RESOURCES.get(resource_id)

    if not resource_data:
        return "Resource Not Found", 404

    # ========================================================
    # RESTRICTED RESOURCE
    # ========================================================

    if resource_id == 303 and session.get("role") != "admin":

        content = """

        <div class="denied">

            <div class="denied-icon">
                🔒
            </div>

            <h1>
                Access Denied
            </h1>

            <p>
                You do not have sufficient privileges
                to access this restricted resource.
            </p>

            <div class="code">
                HTTP 403 — Restricted Resource
            </div>

        </div>

        <script>

            /*
             * Internal resource validation.
             *
             * The current access scope is supplied
             * by the client application.
             */

            const currentScope = "employee";

            fetch("/api/resource/303?scope=" + currentScope)

                .then(response => response.json())

                .then(data => {

                    console.log(
                        "Resource validation:",
                        data
                    );

                })

                .catch(error => {

                    console.log(
                        "Validation request failed:",
                        error
                    );

                });

        </script>

        """

        return page("Access Denied", content), 403

    # ========================================================
    # NORMAL RESOURCE
    # ========================================================

    content = f"""

    <h1>{resource_data["title"]}</h1>

    <div class="subtitle">
        Resource ID: {resource_id}
    </div>

    <div class="card">

        <span class="badge">
            {resource_data["classification"]}
        </span>

        <h3>
            Resource Information
        </h3>

        <p>
            {resource_data["content"]}
        </p>

    </div>

    """

    return page(resource_data["title"], content)


# ============================================================
# API RESOURCE
# ============================================================

@app.route("/api/resource/<int:resource_id>")
def api_resource(resource_id):

    if "username" not in session:

        return jsonify({
            "error": "Authentication required"
        }), 401

    scope = request.args.get(
        "scope",
        "employee"
    )

    resource_data = RESOURCES.get(resource_id)

    if not resource_data:

        return jsonify({
            "error": "Resource not found"
        }), 404

    # ========================================================
    # INTENTIONAL CTF AUTHORIZATION FLAW
    # ========================================================
    #
    # The application trusts the client-controlled
    # "scope" parameter.
    #
    # Employee:
    # scope=employee
    #
    # Admin:
    # scope=admin
    #
    # The server incorrectly trusts this value.
    # ========================================================

    if resource_id == 303 and scope != "admin":

        return jsonify({
            "error": "Restricted resource"
        }), 403

    return jsonify(resource_data)


# ============================================================
# ACCESS.JS
# ============================================================

@app.route("/access.js")
def access_js():

    javascript = """

    const currentScope = "employee";


    async function loadResource(resourceId) {

        const endpoint =
            `/api/resource/${resourceId}?scope=${currentScope}`;

        console.log(
            "Requesting:",
            endpoint
        );

        try {

            const response =
                await fetch(endpoint);

            const data =
                await response.json();

            console.log(
                "Resource loaded:",
                data
            );

        } catch (error) {

            console.log(
                "Request failed:",
                error
            );

        }

    }


    // Normal employee resource.
    // This request is intentionally visible
    // in the browser Network tab.

    loadResource(101);

    """

    return javascript, 200, {
        "Content-Type": "application/javascript"
    }


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )