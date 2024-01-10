import { useState } from "react";
import React from "react";
// import "./forms.css";
import "./Forms1.css";

export const Forms = () => {
  const [formData, setFormData] = useState({
    Email: "",
    Gender: "Female",
    Married: "No",
    Dependents: "0.0",
    Education: "Graduate",
    Self_Employed: "No",
    ApplicantIncome: "2900",
    CoapplicantIncome: "0.0",
    LoanAmount: "71.0",
    Loan_Amount_Term: "360.0",
    Credit_History: "1.0",
    Property_Area: "Rural",
  });

  const [loading, setLoading] = useState(false);
  const [responseText, setResponseText] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setResponseText("Wait while we process your approval...");

    try {
      const response = await fetch("http://127.0.0.1:8000/loan-agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setResponseText(
          "Check your provided email for the loan approval status."
        );
      } else {
        setResponseText("Error processing your request.");
      }
    } catch (error) {
      console.error("Error:", error);
      setResponseText("Error processing your request.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="Predictor">
      <h1>Loan Approval Predictor</h1>
      <div className="Box">
        <form>
          {/* Include form fields based on your requirements */}
          {/* For example: */}
          <label>Email:</label>
          <input
            type="text"
            name="Email"
            value={formData.Email}
            onChange={handleInputChange}
          />

          {/* Add other form fields here... */}

          <label>Gender:</label>
          <input
            type="text"
            name="Gender"
            value={formData.Gender}
            onChange={handleInputChange}
          />

          <label>Dependents:</label>
          <input
            type="number"
            name="Dependents"
            value={formData.Dependents}
            onChange={handleInputChange}
          />

          <label>Education:</label>
          <input
            type="text"
            name="Education"
            value={formData.Education}
            onChange={handleInputChange}
          />

          <label>Self_Employed:</label>
          <input
            type="text"
            name="Self_Employed"
            value={formData.Self_Employed}
            onChange={handleInputChange}
          />

          <label>ApplicantIncome:</label>
          <input
            type="number"
            name="ApplicantIncome"
            value={formData.ApplicantIncome}
            onChange={handleInputChange}
          />

          <label>CoapplicantIncome:</label>
          <input
            type="number"
            name="CoapplicantIncome"
            value={formData.CoapplicantIncome}
            onChange={handleInputChange}
          />

          <label>LoanAmount:</label>
          <input
            type="number"
            name="LoanAmount"
            value={formData.LoanAmount}
            onChange={handleInputChange}
          />

          <label>Loan_Amount_Term:</label>
          <input
            type="text"
            name="Loan_Amount_Term"
            value={formData.Loan_Amount_Term}
            onChange={handleInputChange}
          />

          <label>Credit_History:</label>
          <input
            type="number"
            name="Credit_History"
            value={formData.Credit_History}
            onChange={handleInputChange}
          />

          <label>Property_Area:</label>
          <input
            type="text"
            name="Property_Area"
            value={formData.Property_Area}
            onChange={handleInputChange}
          />

          <label>Married:</label>
          <input
            type="text"
            name="Married"
            value={formData.Married}
            onChange={handleInputChange}
          />

          <button type="button" onClick={handleSubmit} disabled={loading}>
            Submit
          </button>
        </form>
      </div>

      {loading && <p>{responseText}</p>}
      {!loading && responseText && <p>{responseText}</p>}
    </div>
  );
};
