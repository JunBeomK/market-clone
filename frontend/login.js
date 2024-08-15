const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });
  const data = await res.json();
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인되었습니다.");

  window.location.pathname = "/";

  // 로그인이 된 다음에 버튼이 생김 버튼 누르면 작동
  //   const btn = document.createElement("button");
  //   btn.innerText = "상품 가져오기.";
  //   btn.addEventListener("click", async () => {
  //     const res = await fetch("/items", {
  //       headers: {
  //         Authorization: `Bearer ${accessToken}`, // Bearer 액세스토큰 쓸 때 앞에 쓰는 용어
  //       },
  //     });
  //     const data = await res.json(); // json으로 바꿔줌
  //     console.log(data);
  //   });
  //   infoDiv.appendChild(btn);

  //   if (res.status === 200) {
  //     alert("로그인에 성공했습니다.");
  //     console.log(res.status);
  //   } else if (res.status === 401) {
  //     alert("id 혹은 password가 틀렸습니다.");
  //   }
};

form.addEventListener("submit", handleSubmit);
