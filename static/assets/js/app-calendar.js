"use strict";
let direction = "ltr";
isRtl && (direction = "rtl"), document.addEventListener("DOMContentLoaded", function() {
    {
        const f = document.getElementById("calendar"),
            g = document.querySelector(".app-calendar-sidebar"),
            b = document.getElementById("addEventSidebar"),
            h = document.querySelector(".app-overlay"),
            y = {
                Business: "primary",
                Holiday: "success",
                Personal: "danger",
                Family: "warning",
                ETC: "info"
            },
            S = document.querySelector(".offcanvas-title"),
            L = document.querySelector(".btn-toggle-sidebar"),
            E = document.querySelector('button[type="submit"]'),
            k = document.querySelector(".btn-delete-event"),
            w = document.querySelector(".btn-cancel"),
            x = document.querySelector("#eventTitle"),
            q = document.querySelector("#eventStartDate"),
            D = document.querySelector("#eventEndDate"),
            M = document.querySelector("#eventURL"),
            T = $("#eventLabel"),
            P = $("#eventGuests"),
            A = document.querySelector("#eventLocation"),
            F = document.querySelector("#eventDescription"),
            Y = document.querySelector(".allDay-switch"),
            C = document.querySelector(".select-all"),
            H = [].slice.call(document.querySelectorAll(".input-filter")),
            V = document.querySelector(".inline-calendar");
        let a, l = events,
            r = !1,
            e;
        const B = new bootstrap.Offcanvas(b);

        function t(e) {
            return e.id ? "<span class='badge badge-dot bg-" + $(e.element).data("label") + " me-2'> </span>" + e.text : e.text
        }

        function n(e) {
            return e.id ? "<div class='d-flex flex-wrap align-items-center'><div class='avatar avatar-xs me-2'><img src='" + assetsPath + "img/avatars/" + $(e.element).data("avatar") + "' alt='avatar' class='rounded-circle' /></div>" + e.text + "</div>" : e.text
        }
        var d, o;

        function s() {
            var e = document.querySelector(".fc-sidebarToggle-button");
            for (e.classList.remove("fc-button-primary"), e.classList.add("d-lg-none", "d-inline-block", "ps-0"); e.firstChild;) e.firstChild.remove();
            e.setAttribute("data-bs-toggle", "sidebar"), e.setAttribute("data-overlay", ""), e.setAttribute("data-target", "#app-calendar-sidebar"), e.insertAdjacentHTML("beforeend", '<i class="bx bx-menu bx-sm text-body"></i>')
        }
        T.length && T.wrap('<div class="position-relative"></div>').select({
            placeholder: "Select value",
            dropdownParent: T.parent(),
            templateResult: t,
            templateSelection: t,
            minimumResultsForSearch: -1,
            escapeMarkup: function(e) {
                return e
            }
        }), P.length && P.wrap('<div class="position-relative"></div>').select2({
            placeholder: "Select value",
            dropdownParent: P.parent(),
            closeOnSelect: !1,
            templateResult: n,
            templateSelection: n,
            escapeMarkup: function(e) {
                return e
            }
        }), q && (d = q.flatpickr({
            enableTime: !0,
            altFormat: "Y-m-dTH:i:S",
            onReady: function(e, t, n) {
                n.isMobile && n.mobileInput.setAttribute("step", null)
            }
        })), D && (o = D.flatpickr({
            enableTime: !0,
            altFormat: "Y-m-dTH:i:S",
            onReady: function(e, t, n) {
                n.isMobile && n.mobileInput.setAttribute("step", null)
            }
        })), V && (e = V.flatpickr({
            monthSelectorType: "static",
            inline: !0
        }));
        var {
            dayGrid: c,
            interaction: u,
            timeGrid: v,
            list: m
        } = calendarPlugins;
        let i = new Calendar(f, {
            initialView: "dayGridMonth",
            events: function(e, t) {
                let n = function() {
                    let t = [],
                        e = [].slice.call(document.querySelectorAll(".input-filter:checked"));
                    return e.forEach(e => {
                        t.push(e.getAttribute("data-value"))
                    }), t
                }();
                t(l.filter(function(e) {
                    return n.includes(e.extendedProps.calendar.toLowerCase())
                }))
            },
            plugins: [u, c, v, m],
            editable: !0,
            dragScroll: !0,
            dayMaxEvents: 2,
            eventResizableFromStart: !0,
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
            initialDate: new Date,
            navLinks: !0,
            eventClassNames: function({
                event: e
            }) {
                return ["fc-event-" + y[e._def.extendedProps.calendar]]
            },
            dateClick: function(e) {
                e = moment(e.date).format("YYYY-MM-DD");
                p(), B.show(), S && (S.innerHTML = "Add Event"), E.innerHTML = "Add", E.classList.remove("btn-update-event"), E.classList.add("btn-add-event"), k.classList.add("d-none"), q.value = e, D.value = e
            },
            eventClick: function(e) {
                e = e, (a = e.event).url && (e.jsEvent.preventDefault(), window.open(a.url, "_blank")), B.show(), S && (S.innerHTML = "Update Event"), E.innerHTML = "Update", E.classList.add("btn-update-event"), E.classList.remove("btn-add-event"), k.classList.remove("d-none"), x.value = a.title, d.setDate(a.start, !0, "Y-m-d"), !0 === a.allDay ? Y.checked = !0 : Y.checked = !1, null !== a.end ? o.setDate(a.end, !0, "Y-m-d") : o.setDate(a.start, !0, "Y-m-d"), T.val(a.extendedProps.calendar).trigger("change"), void 0 !== a.extendedProps.location && (A.value = a.extendedProps.location), void 0 !== a.extendedProps.guests && P.val(a.extendedProps.guests).trigger("change"), void 0 !== a.extendedProps.description && (F.value = a.extendedProps.description)
            },
            datesSet: function() {
                s()
            },
            viewDidMount: function() {
                s()
            }
        });

        function p() {
            D.value = "", M.value = "", q.value = "", x.value = "", A.value = "", Y.checked = !1, P.val("").trigger("change"), F.value = ""
        }
        i.render(), s(), u = document.getElementById("eventForm"), FormValidation.formValidation(u, {
            fields: {
                eventTitle: {
                    validators: {
                        notEmpty: {
                            message: "Please enter event title "
                        }
                    }
                },
                eventStartDate: {
                    validators: {
                        notEmpty: {
                            message: "Please enter start date "
                        }
                    }
                },
                eventEndDate: {
                    validators: {
                        notEmpty: {
                            message: "Please enter end date "
                        }
                    }
                }
            },
            plugins: {
                trigger: new FormValidation.plugins.Trigger,
                bootstrap5: new FormValidation.plugins.Bootstrap5({
                    eleValidClass: "",
                    rowSelector: function(e, t) {
                        return ".mb-3"
                    }
                }),
                submitButton: new FormValidation.plugins.SubmitButton,
                autoFocus: new FormValidation.plugins.AutoFocus
            }
        }).on("core.form.valid", function() {
            r = !0
        }).on("core.form.invalid", function() {
            r = !1
        }), L && L.addEventListener("click", e => {
            w.classList.remove("d-none")
        }), E.addEventListener("click", e => {
            var t, n;
            E.classList.contains("btn-add-event") ? r && (n = {
                id: i.getEvents().length + 1,
                title: x.value,
                start: q.value,
                end: D.value,
                startStr: q.value,
                endStr: D.value,
                display: "block",
                extendedProps: {
                    location: A.value,
                    guests: P.val(),
                    calendar: T.val(),
                    description: F.value
                }
            }, M.value && (n.url = M.value), Y.checked && (n.allDay = !0), n = n, l.push(n), i.refetchEvents(), B.hide()) : r && (n = {
                id: a.id,
                title: x.value,
                start: q.value,
                end: D.value,
                url: M.value,
                extendedProps: {
                    location: A.value,
                    guests: P.val(),
                    calendar: T.val(),
                    description: F.value
                },
                display: "block",
                allDay: !!Y.checked
            }, (t = n).id = parseInt(t.id), l[l.findIndex(e => e.id === t.id)] = t, i.refetchEvents(), B.hide())
        }), k.addEventListener("click", e => {
            var t;
            t = parseInt(a.id), l = l.filter(function(e) {
                return e.id != t
            }), i.refetchEvents(), B.hide()
        }), b.addEventListener("hidden.bs.offcanvas", function() {
            p()
        }), L.addEventListener("click", e => {
            S && (S.innerHTML = "Add Event"), E.innerHTML = "Add", E.classList.remove("btn-update-event"), E.classList.add("btn-add-event"), k.classList.add("d-none"), g.classList.remove("show"), h.classList.remove("show")
        }), C && C.addEventListener("click", e => {
            e.currentTarget.checked ? document.querySelectorAll(".input-filter").forEach(e => e.checked = 1) : document.querySelectorAll(".input-filter").forEach(e => e.checked = 0), i.refetchEvents()
        }), H && H.forEach(e => {
            e.addEventListener("click", () => {
                document.querySelectorAll(".input-filter:checked").length < document.querySelectorAll(".input-filter").length ? C.checked = !1 : C.checked = !0, i.refetchEvents()
            })
        }), e.config.onChange.push(function(e) {
            i.changeView(i.view.type, moment(e[0]).format("YYYY-MM-DD")), s(), g.classList.remove("show"), h.classList.remove("show")
        })
    }
});