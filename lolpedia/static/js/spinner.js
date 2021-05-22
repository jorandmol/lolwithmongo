$("#btnConfirmLoad").click(function () {
    $("#btnConfirmLoad").html(
        "<span id=\"spinnerBtn\"></span>  Loading data..."
    );
    $("#spinnerBtn").addClass("spinner-border");
    $("#spinnerBtn").addClass("spinner-border-sm");
    $("#spinnerBtn").attr("role", "status");
    $("#spinnerBtn").attr("aria-hidden", "true");
});