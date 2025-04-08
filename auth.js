function handleAuth() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    if (!email || !password) {
      alert("Please fill in all fields.");
      return;
    }
  
    if (isLogin) {
      alert(`Logging in as ${email}`);
      // Redirect to features.html
      window.location.href = "{{ url_for('signup') }}";

    } else {
      alert(`Signing up as ${email}`);
      // You can add signup logic here or also redirect
      window.location.href = "{{ url_for('signup') }}";

    }
  }
  