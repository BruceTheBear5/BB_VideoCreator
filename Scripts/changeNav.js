document.addEventListener("DOMContentLoaded", function() {
  const adminTab = document.getElementById('AdminTab');
  const signTab = document.getElementById('SignTab');
  const profileTab = document.getElementById('ProfileTab');

  const isAdmin = window.getComputedStyle(document.documentElement).getPropertyValue('--isAdmin');
  const isLogin = window.getComputedStyle(document.documentElement).getPropertyValue('--isLogin');


  if (isAdmin.trim() === 'true') {
    adminTab.style.display = 'block';
  }

  if (isLogin.trim() === 'true') {
    signTab.style.display = 'none';
    profileTab.style.display = 'block';
  } else {
    signTab.style.display = 'block';
    profileTab.style.display = 'none';
  }
});
