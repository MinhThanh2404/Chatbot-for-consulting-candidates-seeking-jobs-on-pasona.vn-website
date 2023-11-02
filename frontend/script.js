$(document).ready(function () {
  let mes = localStorage.getItem("cust_mes");
  if (mes) {
    $(".direct-chat-messages").html(mes);
    scroll_to_bottom_chatbot();
  }

  $("#chatbot,.btn-box-tool").on("click", function () {
    $(".direct-chat").fadeToggle();
    scroll_to_bottom_chatbot();
  });

  $(".btn-box-close").on("click", function () {
    clear_mes_hist();
    $(".direct-chat").fadeToggle();
  });

  // free chat with chatbot START

  //Enter key in chat typing area
  $("#input-chat-mess").on("keypress", function (e) {
    if (e.charCode == 13) {
      $("#btn-chat-send").click();
    }
  });

  // Send button
  $(document).on("click", "#btn-chat-send", async function () {
    $(".chat-freechat").toggleClass("chat-hide");

    let mes = $("#input-chat-mess").val();
    $(".direct-chat-messages").append(
      `<div class="direct-chat-msg right">
            <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_2.jpg"
                alt="Message User Image">
            <div class="direct-chat-text">
                <p>${mes}</p>
            </div>
            </div>`
    );
    $(".direct-chat-messages").append(process_bar);
    scroll_to_bottom_chatbot();

    let cust_id = localStorage.getItem("cust_id");
    console.log(cust_id);
    console.log(mes);

    if (mes && cust_id) {
      await analyzeFreeChat(mes, cust_id);
      $("#input-chat-mess").val("");
    } else {
      console.log(cust_id);
    }
  });
  // free chat with chatbot END

  //search job START

  $(document).on("click", ".direct-chat-msg .chat-search", function () {
    console.log("search job");
    console.log(localStorage.getItem("cust_id"));
    console.log($('meta[name="csrf-token"]').attr("content"));

    // Call API Search job
    $.ajaxSetup({
      headers: {
        "x-csrf-token": $('meta[name="csrf-token"]').attr("content"),
      },
    });
    let type = "POST";
    let jobTitle = $(this).parents().data("title");
    let ajaxUrl = $(this).parents().data("link");
    let $searchForm = $(this).closest(".chat-search-form");
    let locationList = [];

    locationList.push($searchForm.find(".search-location").val());

    let formData = {
      job_name: $searchForm.find("input[name=job_name]").val(),
      job_location: locationList,
      job_category: $searchForm.find("select[name=category]").val(),
      job_salary: $searchForm.find("select[name=job_salary]").val(),
    };

    let userMess = "";
    let jobName = $searchForm.find("input[name=job_name]").val();
    let jobLocation = $searchForm
      .find(".search-location")
      .find("option:selected")
      .text();
    let jobIndustry = $searchForm
      .find("select[name=category]")
      .find("option:selected")
      .text();
    let jobSalary = $searchForm
      .find("select[name=job_salary]")
      .find("option:selected")
      .text();

    userMess += jobName ? "Job Title : " + jobName + "<br />" : "";
    userMess += $searchForm.find(".search-location").val()
      ? "Job Location : " + jobLocation + "<br />"
      : "";
    userMess += $searchForm.find("select[name=category]").val()
      ? "Job Industry : " + jobIndustry + "<br />"
      : "";
    userMess += $searchForm.find("select[name=job_salary]").val()
      ? "Job Salary : " + jobSalary + "<br />"
      : "";

    $(".direct-chat-messages").append(
      `<div class="direct-chat-msg right">
            <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_2.jpg"
                alt="Message User Image">
            <div class="direct-chat-text">
                <p>I want to search for jobs with the information below:</p>
                <p>${userMess}</p>
            </div>
            </div>`
    );

    console.log({
      job_name: $searchForm.find("input[name=job_name]").val(),
      job_location: locationList,
      job_category: $searchForm.find("select[name=category]").val(),
      job_salary: $searchForm.find("select[name=job_salary]").val(),
    });
    console.log(localStorage.getItem("cust_id"));
    $.ajax({
      type: type,
      url: ajaxUrl,
      data: formData,
      dataType: "json",
      success: function (result) {
        if (result["msg"] == "success") {
          let jobs = result["jobsChat"];
          if (result["count"] > 0) {
            $(".direct-chat-messages").append(
              `<div class="direct-chat-msg">
                                <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_1.jpg"
                                    alt="Message User Image">
                                <div class="direct-chat-text">
                                    Here is the corresponding job information:<br />
                                    ${jobs}
                                </div>
                            </div>`
            );
            // save search job history
          } else
            $(".direct-chat-messages").append(
              `<div class="direct-chat-msg">
                                <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_1.jpg"
                                    alt="Message User Image">
                                <div class="direct-chat-text">
                                    There is no job matched your request.
                                </div>
                            </div>`
            );
          searchjobHistory(
            localStorage.getItem("cust_id"),
            jobName.trim(),
            processSearchValue(jobIndustry, "Industry"),
            "",
            processSearchValue(jobLocation, "Location"),
            processSearchValue(jobSalary, "Salary")
          );
          bot_ans();

          console.log(result["jobs"]);
          console.log(localStorage.getItem("cust_id"));
        }
      },
      error: function (jqXHR, ajaxOptions, thrownError) {
        alert("No response from server");
      },
      complete: function () {},
      fail: function () {},
    });
  });

  // search job END

  // Cust_info update/insert START

  $(document).on("submit", ".contact-info", function (e) {
    if (!this.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    } else {
      let name = $("#U_Name").val();
      let email = $("#U_Email").val();
      let phone = $("#U_Phone").val();

      console.log(name, email, phone);

      submitUserInfo(name, email, phone);
      // The value of cust_id has been updated at this point
      console.log(localStorage.getItem("cust_id"));

      $(".chat-userInfo").toggleClass("chat-hide");

      $(".direct-chat-messages").append(searchfrom);

      save_mes_hist();
    }
  });
  // Cust_info update/insert END
});

// Rating chatbot + Disable chat START
$(document).on("change", "input[name=rating]", function () {
  console.log($(this).val());
  $("input[name=rating]").each(function () {
    if (!$(this).prop("checked")) {
      $(this).attr("disabled", true);
    }
  });
  let ratingval = $(this).val();

  if (ratingval) {
    enableChatbot(true);
    ratingChatbotUpdate(ratingval, localStorage.getItem("cust_id"));
    bot_ans("Thank you for your rating.");
  }
  // Rating chatbot + Disable chat END
});

function processSearchValue(value, def) {
  if (value.includes(def)) {
    return "";
  } else {
    return value.trim();
  }
}

function submitUserInfo(name, email, phone) {
  $.ajax({
    type: "POST",
    url: ` http://127.0.0.1:8001/userInfo`,
    data: JSON.stringify({
      Name: name,
      Email: email,
      Phone: phone,
    }),
    contentType: "application/json",
    success: function (result) {
      cust_id = result.data;
      console.log(cust_id);
      localStorage.setItem("cust_id", cust_id);
    },
    error: function (jqXHR, ajaxOptions, thrownError) {},
  });
}

function searchjobHistory(
  customer_id,
  keyword,
  industry,
  language,
  location,
  salary
) {
  $.ajax({
    type: "POST",
    url: ` http://127.0.0.1:8001/search`,
    data: JSON.stringify({
      Customer_ID: customer_id,
      Keyword: keyword,
      Location: location,
      Industry: industry,
      Salary: salary,
      Language: language,
    }),
    contentType: "application/json",
    success: function (result) {
      console.log(result);
    },
    error: function (jqXHR, ajaxOptions, thrownError) {},
  });
}

function analyzeFreeChat(mes, cust_id) {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/chat",
    data: JSON.stringify({
      Mes: mes,
      Cust_id: localStorage.getItem("cust_id"),
    }),
    contentType: "application/json",
    success: function (result) {
      $(".progressbar").toggleClass("chat-hide");
      chat_id = result.data.chat_id;
      console.log(result);
      bot_ans(result.data.response ? result.data.response : result.data);
      bot_ans();
    },
    error: function (jqXHR, ajaxOptions, thrownError) {},
  });
}

function showSearchBox() {
  $(".direct-chat-messages").append(
    `<div class="direct-chat-msg right">
            <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_2.jpg"
                alt="Message User Image">
            <div class="direct-chat-text">
                <p>I want to find a job</p>
            </div>
            </div>`
  );
  $(".direct-chat-messages").append(searchfrom);
  save_mes_hist();
}

function enableChatbot(statment) {
  $("#input-chat-mess").prop("disabled", statment);
  $("#btn-chat-send").prop("disabled", statment);
}

function endchat() {
  let rating = `Tell us how you feel when chatting with us. <br />
        <div class="rating">
            <input type="radio" id="star5" name="rating" value="5" /><label class='starrating' for="star5"></label>
            <input type="radio" id="star4" name="rating" value="4" /><label class='starrating' for="star4"></label>
            <input type="radio" id="star3" name="rating" value="3" /><label class='starrating' for="star3"></label>
            <input type="radio" id="star2" name="rating" value="2" /><label class='starrating' for="star2"></label>
            <input type="radio" id="star1" name="rating" value="1" /><label class='starrating' for="star1"></label>
        </div>    
        `;
  bot_ans(rating);
}

function ratingChatbotUpdate(rating, cust_id) {
  console.log(cust_id);
  $.ajax({
    type: "POST",
    url: `http://127.0.0.1:8001/rating_chatbot`,
    data: JSON.stringify({
      Customer_ID: cust_id,
      Rating: rating,
    }),
    contentType: "application/json",
    success: function (result) {
      cust_id = result.data;
      console.log(result);
    },
    error: function (jqXHR, ajaxOptions, thrownError) {},
  });
  save_mes_hist();
}

function bot_ans(ans = "") {
  if (ans) {
    $(".direct-chat-messages").append(
      `<div class="direct-chat-msg">
                    <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_1.jpg"
                        alt="Message User Image">
                    <div class="direct-chat-text">
                        ${ans}
                    </div>
                </div>`
    );
  } else {
    $(".direct-chat-messages").append(
      `<div class="direct-chat-msg">
                    <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_1.jpg"
                        alt="Message User Image">
                    <div class="direct-chat-text">
                        <p>Do you need any more information?</p>
                        <a href='javascript:showSearchBox()' class="chat-next-step" >Search Job</a><br />
                        <a href='javascript:enableChatbot(false)' class="chat-next-step" >Chat with chat-bot</a><br />
                        <a href='javascript:endchat()'  class="chat-next-step" >End chat</a>
                    </div>
                </div>`
    );
  }
  save_mes_hist();
  scroll_to_bottom_chatbot();
}

function save_mes_hist() {
  let hist = $(".direct-chat-messages").html();
  localStorage.setItem("cust_mes", hist);
  scroll_to_bottom_chatbot();
}

function clear_mes_hist() {
  let hist = localStorage.getItem("cust_mes");
  localStorage.setItem("cust_mes", "");
  localStorage.setItem("cust_id", "");
  if (hist)
    $(".direct-chat-messages").html(`<div class="chat-userInfo">
                    <p class="text-black" style="color: black; font-size:small">Hello. Could you please provide
                        information so we can easily contact you?</p>
                    <form class="contact-info" action="{{route('saveData')}}" method="POST">
                        <div class="form-group">
                            <input type="text" name='U_Name' class="form-control" aria-describedby="Name" placeholder="Name" id='U_Name' required>
                        </div>
                        <div class="form-group">
                            <input type="email" name='U_Email' class="form-control" aria-describedby="Email" placeholder="Email" id='U_Email' required>
                        </div>
                        <div class="form-group">
                            <input type="phone" name='U_Phone' class="form-control" aria-describedby="Phone" placeholder="Phone" id='U_Phone' required>
                        </div>
                        <div class="text-center">
                            <button class="btn btn-danger btn-flat" id="submitUserInfo">Submit</button>
                        </div>
                    </form>
                </div>`);
}

function scroll_to_bottom_chatbot() {
  var wtf = $(".direct-chat-messages");
  var height = wtf[0].scrollHeight;
  wtf.scrollTop(height);
}
let searchfrom = `<div class="direct-chat-msg">
                    <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_1.jpg"
                        alt="Message User Image">
                    <div class="direct-chat-text">
                        <p>Hello. Please enter the necessary information to start looking for a job.</p>
                        <div class="chat-search-form">
                            @csrf
                            <div class="search-group">
                                <div class="block-1">
                                    <div class="group-1">
                                        <div class="row">
                                            <div class="col-12">
                                                <div class="form-group">
                                                    <input type="text" name="job_name" class="form-control"
                                                        placeholder="@lang('text1')" maxlength="100" />
                                                </div>
                                            </div>
                                            <div class="col-12">
                                                <!-- using for selected multiple -->
                                                <div class="form-group">
                                                    <select class="form-control search-location" name="location">
                                                        <option value="" selected>@lang('text152')</option>
                                                        @foreach ($locations as $loc)
                                                            <option value="{{ $loc['alias'] }}">
                                                                {{ \Session::get('language') == 'vn' ? $loc['name_vn'] : $loc['name'] }}
                                                            </option>
                                                        @endforeach
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-12">
                                                <div class="form-group">
                                                    <select name="category" class="form-control">
                                                        <option value="" selected>@lang('text157')</option>
                                                        @foreach ($positions as $pos)
                                                            @if (!empty($pos['alias']))
                                                                <option value="{{ $pos['alias'] }}">
                                                                    {{ \Session::get('language') == 'vn' ? $pos['name_vn'] : $pos['name'] }}
                                                                </option>
                                                            @else
                                                                <option value="{{ $pos['alias'] }}" disabled
                                                                    class="disabled">
                                                                    {{ \Session::get('language') == 'vn' ? $pos['name_vn'] : $pos['name'] }}
                                                                </option>
                                                            @endif
                                                        @endforeach
                                                    </select>
                                                </div>
                                            </div>
                                            <div class="col-12">
                                                <div class="form-group">
                                                    <select name="job_salary" class="form-control">
                                                        <option value="" selected>@lang('text158')</option>

                                                        @foreach ($salaries as $sal)
                                                            <option value="{{ $sal['alias'] }}">
                                                                {{ \Session::get('language') == 'vn' ? $sal['name_vn'] : $sal['name'] }}
                                                            </option>
                                                        @endforeach
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="block-2">
                                    <div class="search-button red-button text-center"
                                        data-link="{{ route('getSearchData') }}" data-title="@lang('text6')"
                                        data-offset="">
                                        <button type="button" class="red-button chat-search">@lang('button10')</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
let process_bar = `<div class="progressbar">
                            <div class="direct-chat-msg">
                                <img class="direct-chat-img" src="https://bootdey.com/img/Content/user_1.jpg"
                                    alt="Message User Image">
                                <div class="meter">
                                    <span style="width:100%;"><span class="progress"></span></span>
                                </div>
                            </div>
                        </div>`;
