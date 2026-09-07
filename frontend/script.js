async function predictSalary() {

    const experienceInput =
        document.getElementById("experience");

    const experience =
        parseFloat(experienceInput.value);


    // Check input

    if (isNaN(experience)) {

        alert("Please enter your years of experience.");

        return;
    }


    if (experience < 0) {

        alert("Experience cannot be negative.");

        return;
    }


    try {
        const response = await fetch(
            "/api/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    experience: experience
                })
            }
        );


        const data = await response.json();


        // Display result

        document
            .getElementById("result")
            .classList.remove("hidden");


        document
            .getElementById("salary")
            .innerText =
            "₹ " +
            data.salary.toLocaleString(
                "en-IN",
                {
                    maximumFractionDigits: 2
                }
            );


        document
            .getElementById("message")
            .innerText =
            "For " +
            data.experience +
            " years of experience";


    } catch (error) {

        alert(
            "Unable to connect to the Python server."
        );

        console.error(error);

    }

}