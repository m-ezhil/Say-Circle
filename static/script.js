window.addEventListener("DOMContentLoaded", (ev) => {
  const signupForm = document.getElementById("signup-form");
  const loginForm = document.getElementById("login-form");
  const postsContainer = document.getElementById("posts-container");
  const profile = document.getElementById("profile");
  const logout = document.getElementById("btn-logout");
  const addPostButton = document.getElementById("btn-add-post");
  const editPostButton = document.getElementById("btn-edit-post");
  const addPostModal = document.getElementById("add-post-modal");
  const editPostModal = document.getElementById("edit-post-modal");
  const user = JSON.parse(localStorage.getItem("userdata") || "[]");
  const token = document.cookie.split("jwt_token=").pop();

  function triggerToast(massage, type = "success") {
    if (type == "success") {
      const toastSuccessElement = document.getElementById("toast-success");
      toastSuccessElement
        .getElementsByClassName("toast-body")
        .item(0).innerHTML = massage;
      const toastSuccess = new bootstrap.Toast(toastSuccessElement);
      toastSuccess.show();
    } else if (type == "danger") {
      const toastDangerElement = document.getElementById("toast-danger");
      toastDangerElement
        .getElementsByClassName("toast-body")
        .item(0).innerHTML = massage;
      const toastDanger = new bootstrap.Toast(toastDangerElement);
      toastDanger.show();
    }
  }

  function handlePostDelete(post_id) {
    axios
      .delete("http://127.0.0.1:5050/api/post", {
        data: {
          post_id: post_id,
          user_id: user.id,
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        loadPosts()
        triggerToast(res.data["massage"]);
      });
  }

  function setEditModalData(post_id, title, content) {
    const titleElement = document.getElementById("edit-title");
    const contentElement = document.getElementById("edit-content");
    const postIDElement = document.getElementById("edit-post-id");

    titleElement.value = title;
    contentElement.value = content;
    postIDElement.value = post_id;
  }

  function loadPosts() {
    axios
      .get("http://127.0.0.1:5050/api/posts", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        posts = "";
        for (post of res.data["posts"].sort(
          (a, b) => new Date(b.create_at) - new Date(a.create_at)
        )) {
          postDateTime = new Date(post.create_at);
          posts += `
                <div class="col-12 col-sm-6 col-md-4 col-lg-3 d-flex">
                  <div class="card flex-fill" >
                    <div class="card-header d-flex justify-content-between">
                      <div>
                        <h4>${post.title}</h4>
                        <span class="text-secoundary" style="font-size:.75em">
                          <span class="text-capitalize">${
                            post.owner.user_name
                          } </span> | ${
            postDateTime.toLocaleDateString() +
            " " +
            postDateTime.toLocaleTimeString()
          }
                        </span>
                      </div>
                      <div>
                      ${
                        post.owner.user_id == user.id
                          ? `
                            <div class="dropdown">
                              <button type="button" class="btn" data-bs-toggle="dropdown">
                                <i class="bi bi-three-dots-vertical"></i>
                              </button>
                              <ul class="dropdown-menu">
                                <li><button 
                                  id="post-edit" class="btn dropdown-item post-edit" 
                                  data-bs-toggle="modal"
                                  data-bs-target="#edit-post-modal"
                                  data-post-id="${post.id}"
                                  data-post-title="${post.title}"
                                  data-post-content="${post.content}"
                                  >Edit</button>
                                </li>
                                <li><button class="btn dropdown-item post-delete" data-id="${post.id}">Delete</button></li>
                              </ul>
                            </div>`
                          : ""
                      }
                      </div>
                    </div>
                    <div class="card-body">
                        <p>${post.content}</p>
                    </div>
                  </div>
                </div>
                `;
        }
        postsContainer.innerHTML = posts;
      })
      .catch(res => {
        triggerToast(res.response.data["massage"]||res.response.data["msg"], "danger");
        if(res.status == 401 || res.status == 403){
          setTimeout(() => {
            window.location.href = "http://127.0.0.1:5050/";
          }, 3000);
        }
      });
  }

  document.addEventListener("click", (ev) => {
    if (ev.target.classList.contains("post-delete")) {
      const postId = ev.target.getAttribute("data-id");
      handlePostDelete(postId);
    }
    if (ev.target.classList.contains("post-edit")) {
      const postId = ev.target.getAttribute("data-post-id");
      const postTitle = ev.target.getAttribute("data-post-title");
      const postContent = ev.target.getAttribute("data-post-content");
      setEditModalData(postId, postTitle, postContent);
    }
  });

  if (signupForm) {
    signupForm.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const formData = new FormData(signupForm);
      const data = Object.fromEntries(formData.entries());
      axios.post("http://127.0.0.1:5050/auth/signup", data)
      .then((res) => {
        console.log(res.data);
        triggerToast(res.data["massage"]);
        setTimeout(() => {
          window.location.href = "http://127.0.0.1:5050/";
        }, 3000);
      })
      .catch((res) => {
        console.log(res.response.data);
        triggerToast(res.response.data["massage"] || res.response.data["msg"], "danger");
        if(res.status == 401 || res.status == 403){
          setTimeout(() => {
            window.location.href = "http://127.0.0.1:5050/";
          }, 3000);
        }
      });
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const formData = new FormData(loginForm);
      const data = Object.fromEntries(formData.entries());
      console.log(formData);
      console.log(formData.entries());

      axios.post("http://127.0.0.1:5050/auth/login", data)
      .then((res) => {
        localStorage.setItem("userdata", JSON.stringify(res.data["user"]));
        console.log(res.data);
        triggerToast(res.data["massage"]);
        setTimeout(() => {
          window.location.href = "http://127.0.0.1:5050/home";
        }, 3000);
      })
      .catch((res) => {
        console.log(res.response.data);
        triggerToast(res.response.data["massage"] || res.response.data["msg"], "danger");
      });
    });
  }

  if (profile) {
    profile["src"] = `https://ui-avatars.com/api/?name=${user.user_name}`;
    profile["alt"] = user.user_name;
    profile["title"] = user.user_name;
  }

  if (logout) {
    logout.addEventListener("click", (ev) => {
      axios
        .get("http://127.0.0.1:5050/auth/logout", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          localStorage.clear();
          triggerToast(res.data["massage"]);
          setTimeout(() => {
            window.location.href = "http://127.0.0.1:5050/";
          }, 3000);
        })
        .catch((res) => {
          triggerToast(res.response.data["massage"]||res.response.data["msg"], "danger");
          setTimeout(() => {
            window.location.href = "http://127.0.0.1:5050/";
          }, 3000);
        });
    });
  }

  if (addPostButton) {
    addPostButton.addEventListener("click", (ev) => {
      formData = Object.fromEntries(
        new FormData(document.getElementById("add-post-form")).entries()
      );
      formData["user_id"] = user.id;
      console.log(formData);
      axios
        .post("http://127.0.0.1:5050/api/post", formData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          loadPosts();
          bootstrap.Modal.getInstance(addPostModal).hide();
          triggerToast(res.data["massage"]);
        })
        .catch((res) => {
          triggerToast(res.response.data["massage"]||res.response.data["msg"], "danger");
          if(res.status == 401 || res.status == 403){
            setTimeout(() => {
              window.location.href = "http://127.0.0.1:5050/";
            }, 3000);
          }
        });
    });
  }

  if (editPostButton) {
    editPostButton.addEventListener("click", (ev) => {
      formData = Object.fromEntries(
        new FormData(document.getElementById("edit-post-form")).entries()
      );

      axios
        .patch("http://127.0.0.1:5050/api/post", formData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          loadPosts();
          bootstrap.Modal.getInstance(editPostModal).hide();
          triggerToast(res.data["massage"]);
        })
        .catch((res) => {
          triggerToast(res.response.data["massage"]||res.response.data["msg"], "danger");
          if(res.status == 401 || res.status == 403){
            setTimeout(() => {
              window.location.href = "http://127.0.0.1:5050/";
            }, 3000);
          }
        });
    });
  }

  if (addPostModal) {
    addPostModal.addEventListener("hidden.bs.modal", function () {
      document.getElementById("title").value = "";
      document.getElementById("content").value = "";
    });
  }

  if (postsContainer) {
    loadPosts();
  }
});
