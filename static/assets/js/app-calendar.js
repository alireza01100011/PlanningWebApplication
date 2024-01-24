"use strict";

let direction = "ltr";
if (isRtl) {
    direction = "rtl";
}

document.addEventListener("DOMContentLoaded", function () {
    const calendar_div = document.getElementById("calendar");
    const sidebar = document.querySelector(".app-calendar-sidebar");
    const addEventSidebar = document.getElementById("addEventSidebar");
    const overlay = document.querySelector(".app-overlay");
    const eventTypes = {
        Business: "primary",
        Holiday: "success",
        Personal: "danger",
        Family: "warning",
        ETC: "info"
    };
    const sidebarTitle = document.querySelector(".offcanvas-title");
    const toggleSidebarButton = document.querySelector(".btn-toggle-sidebar");
    const submitButton = document.querySelector('button[type="submit"]');
    const deleteButton = document.querySelector(".btn-delete-event");
    const cancelButton = document.querySelector(".btn-cancel");
    const eventTitleInput = document.querySelector("#eventTitle");
    const eventStartDateInput = document.querySelector("#eventStartDate");
    const eventEndDateInput = document.querySelector("#eventEndDate");
    const eventURLInput = document.querySelector("#eventURL");
    const eventLabelSelect = $("#eventLabel");
    const eventReminderSelect = $("#eventReminder");
    const eventLocationInput = document.querySelector("#eventLocation");
    const eventDescriptionInput = document.querySelector("#eventDescription");
    const allDaySwitch = document.querySelector(".allDay-switch");
    const selectAllCheckbox = document.querySelector(".select-all");
    const filterInputs = [].slice.call(document.querySelectorAll(".input-filter"));
    const inlineCalendar = document.querySelector(".inline-calendar");

    let events = [];
    let isFormValid = false;
    let currentEvent;

    const addEventSidebarOffcanvas = new bootstrap.Offcanvas(addEventSidebar);

    function formatLabelOption(option) {
        if (option.id) {
            return `<span class='badge badge-dot bg-${$(option.element).data("label")} me-2'> </span>${option.text}`;
        }
        return option.text;
    }

    function formatGuestOption(option) {
        if (option.id) {
            return `<div class='d-flex flex-wrap align-items-center'><div class='avatar avatar-xs me-2'><img src='${assetsPath}img/avatars/${$(option.element).data("avatar")}' alt='avatar' class='rounded-circle' /></div>${option.text}</div>`;
        }
        return option.text;
    }

    function setupSidebarToggleButton() {
        const toggleButton = document.querySelector(".fc-sidebarToggle-button");
        toggleButton.classList.remove("fc-button-primary");
        toggleButton.classList.add("d-lg-none", "d-inline-block", "ps-0");
        while (toggleButton.firstChild) {
            toggleButton.firstChild.remove();
        }
        toggleButton.setAttribute("data-bs-toggle", "sidebar");
        toggleButton.setAttribute("data-overlay", "");
        toggleButton.setAttribute("data-target", "#app-calendar-sidebar");
        toggleButton.insertAdjacentHTML("beforeend", '<i class="bx bx-menu bx-sm text-body"></i>');
    }

    if (eventLabelSelect.length) {
        eventLabelSelect.wrap('<div class="position-relative"></div>').select({
            placeholder: "Select value",
            dropdownParent: eventLabelSelect.parent(),
            templateResult: formatLabelOption,
            templateSelection: formatLabelOption,
            minimumResultsForSearch: -1,
            escapeMarkup: function (markup) {
                return markup;
            }
        });
    }

    if (eventReminderSelect.length) {
        eventReminderSelect.wrap('<div class="position-relative"></div>').select2({
            placeholder: "Select value",
            dropdownParent: eventReminderSelect.parent(),
            closeOnSelect: false,
            templateResult: formatGuestOption,
            templateSelection: formatGuestOption,
            escapeMarkup: function (markup) {
                return markup;
            }
        });
    }

    if (eventStartDateInput) {
        const startDatePicker = eventStartDateInput.flatpickr({
            enableTime: true,
            altFormat: "Y-m-dTH:i:S",
            onReady: function (selectedDates, dateStr, instance) {
                if (instance.isMobile) {
                    instance.mobileInput.setAttribute("step", null);
                }
            }
        });
    }

    if (eventEndDateInput) {
        const endDatePicker = eventEndDateInput.flatpickr({
            enableTime: true,
            altFormat: "Y-m-dTH:i:S",
            onReady: function (selectedDates, dateStr, instance) {
                if (instance.isMobile) {
                    instance.mobileInput.setAttribute("step", null);
                }
            }
        });
    }

    if (inlineCalendar) {
        const inlineDatePicker = inlineCalendar.flatpickr({
            monthSelectorType: "static",
            inline: true
        });
    }

    const { dayGrid, interaction, timeGrid, list } = calendarPlugins;

    const calendar = new Calendar(calendar_div, {
        initialView: "dayGridMonth",
        events: function (fetchInfo, successCallback) {
            const selectedFilters = function () {
                const filters = [];
                const checkedFilters = [].slice.call(document.querySelectorAll(".input-filter:checked"));
                checkedFilters.forEach(filter => {
                    filters.push(filter.getAttribute("data-value"));
                });
                return filters;
            }();
            const filteredEvents = events.filter(function (event) {
                return selectedFilters.includes(event.extendedProps.calendar.toLowerCase());
            });
            successCallback(filteredEvents);
        },
        plugins: [interaction, dayGrid, timeGrid, list],
        editable: true,
        dragScroll: true,
        dayMaxEvents: 2,
        eventResizableFromStart: true,
        customButtons: {
            sidebarToggle: {
                text: "Sidebar"
            }
        },
        headerToolbar: {
            start: "sidebarToggle, prev,next, title",
            end: "dayGridMonth,timeGridWeek,timeGridDay,listMonth"
        },
        direction: direction,
        initialDate: new Date(),
        navLinks: true,
        eventClassNames: function ({ event }) {
            return ["fc-event-" + eventTypes[event._def.extendedProps.calendar]];
        },
        dateClick: function (clickInfo) {
            const selectedDate = moment(clickInfo.date).format("YYYY-MM-DD");
            resetForm();
            addEventSidebarOffcanvas.show();
            if (sidebarTitle) {
                sidebarTitle.innerHTML = "Add Event";
            }
            submitButton.innerHTML = "Add";
            submitButton.classList.remove("btn-update-event");
            submitButton.classList.add("btn-add-event");
            deleteButton.classList.add("d-none");
            eventStartDateInput.value = selectedDate;
            eventEndDateInput.value = selectedDate;
        },
        eventClick: function (clickInfo) {
            const clickedEvent = clickInfo.event;
            const event = clickedEvent.event;
            if (event.url) {
                clickInfo.jsEvent.preventDefault();
                window.open(event.url, "_blank");
            }
            addEventSidebarOffcanvas.show();
            if (sidebarTitle) {
                sidebarTitle.innerHTML = "Update Event";
            }
            submitButton.innerHTML = "Update";
            submitButton.classList.add("btn-update-event");
            submitButton.classList.remove("btn-add-event");
            deleteButton.classList.remove("d-none");
            eventTitleInput.value = event.title;
            eventStartDateInput.flatpickr.setDate(event.start, true, "Y-m-d");
            if (event.allDay) {
                allDaySwitch.checked = true;
            } else {
                allDaySwitch.checked = false;
            }
            if (event.end !== null) {
                eventEndDateInput.flatpickr.setDate(event.end, true, "Y-m-d");
            } else {
                eventEndDateInput.flatpickr.setDate(event.start, true, "Y-m-d");
            }
            eventLabelSelect.val(event.extendedProps.calendar).trigger("change");
            if (event.extendedProps.location !== undefined) {
                eventLocationInput.value = event.extendedProps.location;
            }
            if (event.extendedProps.guests !== undefined) {
                eventReminderSelect.val(event.extendedProps.guests).trigger("change");
            }
            if (event.extendedProps.description !== undefined) {
                eventDescriptionInput.value = event.extendedProps.description;
            }
        },
        datesSet: function () {
            setupSidebarToggleButton();
        },
        viewDidMount: function () {
            setupSidebarToggleButton();
        }
    });

    function resetForm() {
        eventEndDateInput.value = "";
        eventURLInput.value = "";
        eventStartDateInput.value = "";
        eventTitleInput.value = "";
        eventLocationInput.value = "";
        allDaySwitch.checked = false;
        eventReminderSelect.val("").trigger("change");
        eventDescriptionInput.value = "";
    }

    calendar.render();
    setupSidebarToggleButton();

    const eventForm = document.getElementById("eventForm");

    FormValidation.formValidation(eventForm, {
        fields: {
            eventTitle: {
                validators: {
                    notEmpty: {
                        message: "Please enter event title"
                    }
                }
            },
            eventStartDate: {
                validators: {
                    notEmpty: {
                        message: "Please enter start date"
                    }
                }
            },
            eventEndDate: {
                validators: {
                    notEmpty: {
                        message: "Please enter end date"
                    }
                }
            }
        },
        plugins: {
            trigger: new FormValidation.plugins.Trigger(),
            bootstrap5: new FormValidation.plugins.Bootstrap5({
                eleValidClass: "",
                rowSelector: function (field, ele) {
                    return ".mb-3";
                }
            }),
            submitButton: new FormValidation.plugins.SubmitButton(),
            autoFocus: new FormValidation.plugins.AutoFocus()
        }
    })
        .on("core.form.valid", function () {
            isFormValid = true;
        })
        .on("core.form.invalid", function () {
            isFormValid = false;
        });

    if (toggleSidebarButton) {
        toggleSidebarButton.addEventListener("click", function (e) {
            cancelButton.classList.remove("d-none");
        });
    }

    submitButton.addEventListener("click", function (e) {
        if (submitButton.classList.contains("btn-add-event")) {
            if (isFormValid) {
                // Send Event To Sever
                const form_url = eventForm.getAttribute('action')
                const form_data = {
                    title: eventTitleInput.value,
                    start: eventStartDateInput.value,
                    end: eventEndDateInput.value,
                    startStr: eventStartDateInput.value,
                    endStr: eventEndDateInput.value,
                    description: eventDescriptionInput.value
                };

                var xhr = new XMLHttpRequest();
                xhr.open("POST", form_url, true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.send(JSON.stringify(form_data));
                // - Send Event To Sever

                const newEvent = {
                    id: calendar.getEvents().length + 1,
                    title: eventTitleInput.value,
                    start: eventStartDateInput.value,
                    end: eventEndDateInput.value,
                    startStr: eventStartDateInput.value,
                    endStr: eventEndDateInput.value,
                    display: "block",
                    extendedProps: {
                        location: eventLocationInput.value,
                        calendar: eventLabelSelect.val(),
                        description: eventDescriptionInput.value
                    }
                };
                if (eventURLInput.value) {
                    newEvent.url = eventURLInput.value;
                }
                if (allDaySwitch.checked) {
                    newEvent.allDay = true;
                }
                events.push(newEvent);
                calendar.refetchEvents();
                addEventSidebarOffcanvas.hide();
            }
        } else {
            if (isFormValid) {
                const updatedEvent = {
                    id: currentEvent.id,
                    title: eventTitleInput.value,
                    start: eventStartDateInput.value,
                    end: eventEndDateInput.value,
                    url: eventURLInput.value,
                    extendedProps: {
                        location: eventLocationInput.value,
                        guests: eventReminderSelect.val(),
                        calendar: eventLabelSelect.val(),
                        description: eventDescriptionInput.value
                    },
                    display: "block",
                    allDay: allDaySwitch.checked
                };
                updatedEvent.id = parseInt(updatedEvent.id);
                events[events.findIndex(event => event.id === updatedEvent.id)] = updatedEvent;
                calendar.refetchEvents();
                addEventSidebarOffcanvas.hide();
            }
        }
    });

    deleteButton.addEventListener("click", function (e) {
        const eventId = parseInt(currentEvent.id);
        events = events.filter(function (event) {
            return event.id != eventId;
        });
        calendar.refetchEvents();
        addEventSidebarOffcanvas.hide();
    });

    addEventSidebar.addEventListener("hidden.bs.offcanvas", function () {
        resetForm();
    });

    toggleSidebarButton.addEventListener("click", function (e) {
        if (sidebarTitle) {
            sidebarTitle.innerHTML = "Add Event";
        }
        submitButton.innerHTML = "Add";
        submitButton.classList.remove("btn-update-event");
        submitButton.classList.add("btn-add-event");
        deleteButton.classList.add("d-none");
        sidebar.classList.remove("show");
        overlay.classList.remove("show");
    });

    selectAllCheckbox.addEventListener("click", function (e) {
        if (e.currentTarget.checked) {
            document.querySelectorAll(".input-filter").forEach(function (input) {
                input.checked = true;
            });
        } else {
            document.querySelectorAll(".input-filter").forEach(function (input) {
                input.checked = false;
            });
        }
        calendar.refetchEvents();
    });

    filterInputs.forEach(function (input) {
        input.addEventListener("click", function () {
            if (document.querySelectorAll(".input-filter:checked").length < document.querySelectorAll(".input-filter").length) {
                selectAllCheckbox.checked = false;
            } else {
                selectAllCheckbox.checked = true;
            }
            calendar.refetchEvents();
        });
    });

    e.config.onChange.push(function (selectedDates) {
        calendar.changeView(calendar.view.type, moment(selectedDates[0]).format("YYYY-MM-DD"));
        setupSidebarToggleButton();
        sidebar.classList.remove("show");
        overlay.classList.remove("show");
    });
});
