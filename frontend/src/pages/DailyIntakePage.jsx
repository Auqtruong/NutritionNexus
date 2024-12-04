import React from "react";
import DailyIntake from "../components/DailyIntake";

const DailyIntakePage = () => {
  return (
    <div>
      <header>
        <h1>Daily Intake Tracker</h1>
      </header>
      {/* TODO: Add additional features like filtering, extra UI, etc.*/}
      <DailyIntake />
    </div>
  );
};

export default DailyIntakePage;