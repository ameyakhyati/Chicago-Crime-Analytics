let editingCaseNumber = null;
let selectedCaseNumber = null;

async function getCrimes() {
    try {
        const response = await fetch("/api/crimes");
        const result = await response.json();

        if (!response.ok || !result.success) {throw new Error(result.message || "Failed to fetch crime records.");}

        displayCrimeCount(result.count);
        displayCrimes(result.data);
    } catch (error) {
        console.error("Error fetching crimes:", error);
        document.getElementById("crime-table-container").innerHTML = `<p>Failed to load crime records.</p>`;
    }
}

function displayCrimeCount(count) {
    document.getElementById("crime-record-count").textContent = `Total Crime Records: ${count}`;
}

function displayCrimes(crimes) {
    const container = document.getElementById("crime-table-container");
    selectedCaseNumber = null;

    if (crimes.length === 0) {
        container.innerHTML = `<p>No crime records found.</p>`;
        return;
    }

    let tableHTML = `
        <div class="table-responsive">
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col">Case Number</th>
                        <th scope="col">Incident Date</th>
                        <th scope="col">Incident Day</th>
                        <th scope="col">Crime Type</th>
                        <th scope="col">Description</th>
                        <th scope="col">Location</th>
                        <th scope="col">Arrest</th>
                        <th scope="col">Domestic</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
    `;

    crimes.forEach((crime) => {
        tableHTML += `
            <tr class="crime-row" data-case-number="${crime.CASE_NUMBER}">
                <td>${crime.CASE_NUMBER}</td>
                <td>${crime.INCIDENT_DATE}</td>
                <td>${crime.INCIDENT_DAYOFWEEK}</td>
                <td>${crime.PRIMARY_TYPE}</td>
                <td>${crime.DESCRIPTION}</td>
                <td>${crime.LOCATION_DESC}</td>
                <td>${crime.ARREST ? "Yes" : "No"}</td>
                <td>${crime.DOMESTIC ? "Yes" : "No"}</td>
            </tr>
        `;
    });

    tableHTML += ` </tbody> </table> </div> `;

    container.innerHTML = tableHTML;

    container.querySelectorAll(".crime-row").forEach((row) => {
        row.addEventListener("click", () => {
            container.querySelectorAll(".crime-row").forEach((r) => {
                r.classList.remove("table-success", "selected");
            });

            row.classList.add("table-success", "selected");
            selectedCaseNumber = row.dataset.caseNumber;
        });
    });
}


function getSelectedCaseNumber() {
    if (!selectedCaseNumber) {
        showMessageModal("No Crime Selected", "Please select a crime record first.");
        return null;
    }

    return selectedCaseNumber;
}


function resetCrimeModal() {
    editingCaseNumber = null;

    document.getElementById("crime-form").reset();
    document.querySelector("#crime-modal h2").textContent = "Add Crime";
    document.getElementById("save-crime-btn").textContent = "Save Crime";
    document.getElementById("case-number").readOnly = false;
}

function openCrimeModal() {
    resetCrimeModal();

    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById("crime-modal"));
    modal.show();
}

function closeCrimeModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById("crime-modal"));

    if (modal) {
        modal.hide();
    }
}

async function fetchCrime(caseNumber) {
    const response = await fetch(`/api/crimes/${encodeURIComponent(caseNumber)}`);
    const result = await response.json();

    if (!response.ok || !result.success) {
        throw new Error(result.message || "Failed to fetch crime record.");
    }

    return result.data;
}

async function editSelectedCrime() {
    const caseNumber = getSelectedCaseNumber();

    if (!caseNumber) {
        return;
    }

    try {
        const crime = await fetchCrime(caseNumber);

        editingCaseNumber = caseNumber;
        populateCrimeForm(crime);

        document.querySelector("#crime-modal h2").textContent = "Edit Crime";
        document.getElementById("save-crime-btn").textContent = "Update Crime";
        document.getElementById("case-number").readOnly = true;

        const modal = bootstrap.Modal.getOrCreateInstance( document.getElementById("crime-modal"));

        modal.show();
    } catch (error) {
        console.error("Error loading crime:", error);
        showMessageModal( "Error", `Failed to load crime record: ${error.message}`);
    }
}


async function getSelectedCrime() {
    const caseNumber = getSelectedCaseNumber();

    if (!caseNumber) {
        return;
    }

    try {
        const crime = await fetchCrime(caseNumber);

        displayCrimeRecord(crime);
        openGetCrimeModal();
    } catch (error) {
        console.error("Error fetching crime record:", error);
        showMessageModal("Error",`Failed to load crime record: ${error.message}`);
    }
}

function displayCrimeRecord(crime) {
    const resultContainer = document.getElementById("get-crime-result");

    resultContainer.innerHTML = `
        <div class="crime-record-box">
            <div class="crime-detail">
                <strong>Case Number</strong>
                <span>${crime.CASE_NUMBER}</span>
            </div>
            <div class="crime-detail">
                <strong>Incident Date</strong>
                <span>${crime.INCIDENT_DATE}</span>
            </div>
            <div class="crime-detail">
                <strong>Incident Day</strong>
                <span>${crime.INCIDENT_DAYOFWEEK}</span>
            </div>
            <div class="crime-detail">
                <strong>Incident Time</strong>
                <span>${crime.INCIDENT_TIME}</span>
            </div>
            <div class="crime-detail">
                <strong>Incident Month</strong>
                <span>${crime.INCIDENT_MONTH}</span>
            </div>
            <div class="crime-detail">
                <strong>Incident Year</strong>
                <span>${crime.INCIDENT_YEAR}</span>
            </div>
            <div class="crime-detail">
                <strong>Primary Type</strong>
                <span>${crime.PRIMARY_TYPE}</span>
            </div>
            <div class="crime-detail">
                <strong>Description</strong>
                <span>${crime.DESCRIPTION}</span>
            </div>
            <div class="crime-detail">
                <strong>Location</strong>
                <span>${crime.LOCATION_DESC}</span>
            </div>
            <div class="crime-detail">
                <strong>Last Updated</strong>
                <span>${crime.DATE_OF_UPDATE}</span>
            </div>
            <div class="crime-detail">
                <strong>Block</strong>
                <span>${crime.BLOCK}</span>
            </div>
            <div class="crime-detail">
                <strong>IUCR Code</strong>
                <span>${crime.IUCR_CODE}</span>
            </div>
            <div class="crime-detail">
                <strong>Arrest</strong>
                <span>${crime.ARREST ? "Yes" : "No"}</span>
            </div>
            <div class="crime-detail">
                <strong>Domestic</strong>
                <span>${crime.DOMESTIC ? "Yes" : "No"}</span>
            </div>
            <div class="crime-detail">
                <strong>Beat</strong>
                <span>${crime.BEAT_NUM}</span>
            </div>
            <div class="crime-detail">
                <strong>District</strong>
                <span>${crime.DISTRICT_CODE}</span>
            </div>
            <div class="crime-detail">
                <strong>Ward</strong>
                <span>${crime.WARD_NO}</span>
            </div>
            <div class="crime-detail">
                <strong>Community</strong>
                <span>${crime.COMMUNITY_CODE}</span>
            </div>
            <div class="crime-detail">
                <strong>FBI Code</strong>
                <span>${crime.FBI_CODE}</span>
            </div>
            <div class="crime-detail">
                <strong>Latitude</strong>
                <span>${crime.LATITUDE}</span>
            </div>
            <div class="crime-detail">
                <strong>Longitude</strong>
                <span>${crime.LONGITUDE}</span>
            </div>
        </div>
    `;
}


function openGetCrimeModal() {
    const modal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById("get-crime-modal")
    );

    modal.show();
}


function populateCrimeForm(crime) {
    document.getElementById("case-number").value = crime.CASE_NUMBER || "";
    document.getElementById("incident-date").value = crime.INCIDENT_DATE || "";
    document.getElementById("incident-time").value = crime.INCIDENT_TIME ? crime.INCIDENT_TIME.substring(0, 5) : "";

    document.getElementById("block").value = crime.BLOCK || "";
    document.getElementById("iucr-code").value = crime.IUCR_CODE || "";
    document.getElementById("primary-type").value = crime.PRIMARY_TYPE || "";
    document.getElementById("description").value = crime.DESCRIPTION || "";
    document.getElementById("location-desc").value = crime.LOCATION_DESC || "";
    document.getElementById("fbi-code").value = crime.FBI_CODE || "";

    document.getElementById("beat-num").value = crime.BEAT_NUM ?? "";
    document.getElementById("district-code").value = crime.DISTRICT_CODE ?? "";
    document.getElementById("ward-no").value = crime.WARD_NO ?? "";
    document.getElementById("community-code").value = crime.COMMUNITY_CODE ?? "";

    document.getElementById("arrest").value = crime.ARREST ? "true" : "false";
    document.getElementById("domestic").value = crime.DOMESTIC ? "true" : "false";

    document.getElementById("x-coordinate").value = crime.X_COORDINATE ?? "";
    document.getElementById("y-coordinate").value = crime.Y_COORDINATE ?? "";
    document.getElementById("latitude").value = crime.LATITUDE ?? "";
    document.getElementById("longitude").value = crime.LONGITUDE ?? "";
    document.getElementById("location").value = crime.LOCATION || "";
}


async function saveCrime(event) {
    event.preventDefault();

    const form = document.getElementById("crime-form");
    const formData = new FormData(form);
    const crimeData = Object.fromEntries(formData.entries());

    crimeData.ARREST = crimeData.ARREST === "true";
    crimeData.DOMESTIC = crimeData.DOMESTIC === "true";

    const numericFields = [ "BEAT_NUM", "DISTRICT_CODE", "WARD_NO", "COMMUNITY_CODE", "X_COORDINATE", "Y_COORDINATE", "LATITUDE", "LONGITUDE"];

    numericFields.forEach((field) => {
        if (crimeData[field] !== undefined && crimeData[field] !== "") {
            crimeData[field] = Number(crimeData[field]);
        }
    });

    const incidentDate = new Date(`${crimeData.INCIDENT_DATE}T${crimeData.INCIDENT_TIME}`);

    if (isNaN(incidentDate.getTime())) {
        showMessageModal("Invalid Date","Please provide a valid incident date and time.");
        return;
    }

    crimeData.INCIDENT_YEAR = incidentDate.getFullYear();
    crimeData.INCIDENT_MONTH = incidentDate.getMonth() + 1;
    crimeData.INCIDENT_DAYOFWEEK = incidentDate.toLocaleDateString("en-US",{ weekday: "long" });

    if (crimeData.INCIDENT_TIME && crimeData.INCIDENT_TIME.length === 5) {crimeData.INCIDENT_TIME += ":00";}

    crimeData.DATE_OF_UPDATE = new Date().toISOString().slice(0, 19).replace("T", " ");

    const isEditing = editingCaseNumber !== null;
    const url = isEditing
        ? `/api/crimes/${encodeURIComponent(editingCaseNumber)}`
        : "/api/crimes";
    const method = isEditing ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(crimeData)
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(
                result.message ||
                (isEditing
                    ? "Failed to update crime record."
                    : "Failed to create crime record.")
            );
        }

        closeCrimeModal();
        await getCrimes();

        showMessageModal(
            isEditing ? "Crime Updated" : "Crime Added",
            isEditing
                ? "Crime record updated successfully."
                : "Crime record added successfully."
        );
    } catch (error) {
        console.error(
            isEditing ? "Error updating crime:" : "Error creating crime:",
            error
        );

        showMessageModal("Error",
            error.message ||
            (isEditing
                ? "Failed to update crime record."
                : "Failed to create crime record.")
        );
    }
}



function deleteSelectedCrime() {
    const caseNumber = getSelectedCaseNumber();

    if (!caseNumber) {
        return;
    }

    document.getElementById("delete-crime-message").textContent = `Are you sure you want to delete crime ${caseNumber}?`;
    const modal = bootstrap.Modal.getOrCreateInstance( document.getElementById("delete-crime-modal"));

    modal.show();
}

async function confirmDeleteCrime() {
    const caseNumber = selectedCaseNumber;

    if (!caseNumber) {
        return;
    }

    try {
        const response = await fetch(`/api/crimes/${encodeURIComponent(caseNumber)}`, { method: "DELETE" });
        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.message || "Failed to delete crime record.");}

        const modal = bootstrap.Modal.getInstance(document.getElementById("delete-crime-modal"));
        if (modal) {
            modal.hide();
        }

        await getCrimes();
        showMessageModal("Crime Deleted","Crime record deleted successfully.");

    } catch (error) {
        console.error("Error deleting crime:", error);

        showMessageModal( "Error",`Failed to delete crime: ${error.message}`);
    }
}

async function loadCrimeOptions() {
    try {
        const response = await fetch("/api/crime-options");
        const result = await response.json();

        if (!response.ok || !result.success) { throw new Error(result.message || "Failed to load crime options."); }

        populateIUCR(result.data.iucr);
        populateBeats(result.data.beats);
        populateDistricts(result.data.districts);
        populateWards(result.data.wards);
        populateCommunities(result.data.communities);
    } catch (error) {
        console.error("Error loading crime options:", error);
        showMessageModal("Error",`Failed to load crime options: ${error.message}`);
    }
}


function populateIUCR(data) {
    const select = document.getElementById("iucr-code");

    data.forEach((item) => {
        const option = document.createElement("option");

        option.value = item.IUCR_CODE;
        option.textContent = `${item.IUCR_CODE} - ${item.PRIMARY_TYPE} - ${item.DESCRIPTION}`;

        option.dataset.primaryType = item.PRIMARY_TYPE;
        option.dataset.description = item.DESCRIPTION;

        select.appendChild(option);
    });
}

function populateBeats(data) {
    const select = document.getElementById("beat-num");

    data.forEach((beat) => {
        const option = document.createElement("option");
        option.value = beat;
        option.textContent = beat;
        select.appendChild(option);
    });
}

function populateDistricts(data) {
    const select = document.getElementById("district-code");

    data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.DISTRICT_CODE;
        option.textContent =`${item.DISTRICT_CODE} - ${item.DISTRICT_NAME}`;
        select.appendChild(option);
    });
}

function populateWards(data) {
    const select = document.getElementById("ward-no");

    data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.WARD_NO;
        option.textContent = `${item.WARD_NO} - ${item.ALDERMAN}`;
        select.appendChild(option);
    });
}

function populateCommunities(data) {
    const select = document.getElementById("community-code");

    data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.COMMUNITY_CODE;
        option.textContent = `${item.COMMUNITY_CODE} - ${item.COMMUNITY_NAME}`;
        select.appendChild(option);
    });
}

document.getElementById("iucr-code").addEventListener("change", function() {
    const selectedOption = this.options[this.selectedIndex];

    document.getElementById("primary-type").value = selectedOption.dataset.primaryType || "";

    document.getElementById("description").value = selectedOption.dataset.description || "";
});

function showMessageModal(title, message) {
    document.getElementById("success-modal-title").textContent = title;
    document.getElementById("success-modal-message").textContent = message;

    const modal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById("success-modal")
    );

    modal.show();
}


document.getElementById("add-crime-btn").addEventListener("click", openCrimeModal);

document.getElementById("get-crime-btn").addEventListener("click", getSelectedCrime);

document.getElementById("edit-crime-btn").addEventListener("click", editSelectedCrime);

document.getElementById("delete-crime-btn").addEventListener("click", deleteSelectedCrime);

document.getElementById("confirm-delete-btn").addEventListener("click", confirmDeleteCrime);

document.getElementById("crime-form").addEventListener("submit", saveCrime);

document.getElementById("crime-modal").addEventListener("hidden.bs.modal", resetCrimeModal);


loadCrimeOptions();
getCrimes();