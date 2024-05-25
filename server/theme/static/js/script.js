window.onload = function() {
    const search = document.getElementById("search")
    search.addEventListener('enter', function handleEnterKey(event) {
        // Kiểm tra nếu phím được nhấn là Enter (mã phím 13)
        if (event.keyCode === 13) {
          // Lấy giá trị từ thẻ input
          const searchValue = document.getElementById("searchInput").value;
      
          // Tạo một đối tượng FormData
          const formData = new FormData();
          formData.append("searched", searchValue);
      
          // Gửi yêu cầu POST tới trang "search"
          fetch("{% url 'search' %}", {
            method: "POST",
            headers: {
              "X-CSRFToken": "{{ csrf_token }}",
            },
            body: formData,
          })
        }
      }
    )
    function submitAddToCartForm() {
        document.getElementById('add-to-cart-form').submit();
    }
}
// Prevent the default behavior of the anchor tag inside the div
document.querySelectorAll('.clickable-div a').forEach(anchor => {
    anchor.addEventListener('click', function(event) {
        event.preventDefault();
    });
});

